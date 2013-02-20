function [] = flowmovie(inFile, outDir, grayScale, maxFrames)

% flowmovie(inFile, outDir, grayScale, maxFrames)
%
% Computes the flow between every two successive frames of the given input
% movie file and stores the computed flow as .hdf5 to the output directory.
%
% If the parameter `grayScale` is set to 0 (the default), then the input data
% is fed as it is into the flow calculation procedure. Else, it is gray-scaled
% just before using `rgb2gray()`.
%
% The parameter `maxFrames` controls the maximum number of frames that will
% have their optical flow calculated for. By default, use all available frames.
%
% This function is based on the original work from Murali M. Chakka and leads
% to *exact* the same results as his old implementation.
%
% Improved by Andre Anjos <andre.anjos@idiap.ch>
% Thu 15 Nov 2012 16:55:36 CET -- initial version
% Wed 20 Feb 2013 15:58:22 CET -- optional pre-gray-scaling and max frames

if nargin == 0
  disp('usage: flowmovie <input-file> <output-dir> <pre-grayscale> <frames>');
  return;
end

if nargin < 3
  grayScale = 0;
else
  grayScale = str2num(grayScale);
end

addpath('mex');

disp(sprintf('Loading contents of %s...', inFile));
videoObject = mmreader(inFile);
frames = read(videoObject) ; % frames will be uint8 at this point
N = videoObject.NumberOfFrames;
isColor = 1; % movie files are always colored

% Use this to load HDF5 files produced by Bob instead
%frames = hdf5read(inFile, 'array');
%isColor = size(size(frames),2) == 4;
%isColor = size(size(frames),2) == 4;
%if isColor == 1
%  frames = permute(frames, [2 1 3 4]);
%  N = size(frames,4);
%else
%  frames = permute(frames, [2 1 3]);
%  N = size(frames,3);
%end

disp(sprintf('Loaded %d frames.', N));

if nargin < 4
  N = size(frames,4);
else
  N = str2num(maxFrames);
end

disp(sprintf('Running flow analysis for %d frames:', N));

if grayScale ~= 0 && isColor == 1
  % Convert frames to grayscale
  for i = 1 : N
    disp(sprintf(' * Converting frame #%d to grayscale', i));
    grayFrames(:, :, i) = rgb2gray(frames(:, :, :, i));
  end
  frames = grayFrames;
  isColor = 0;
end

% Set optical flow parameters (see Coarse2FineTwoFrames.m for the definition of
% the parameters)
alpha = 1.0;
ratio = 0.5;
minWidth = 40;
nOuterFPIterations = 4;
nInnerFPIterations = 1;
nIterations = 20;

para = [alpha,ratio,minWidth,nOuterFPIterations,nInnerFPIterations,nIterations];

for i = 1 : N-1
  disp(sprintf(' * Evaluating flow between frames #%d -> #%d', i, i+1));
  if isColor == 1
    im1 = im2double(frames(:, :, :, i));
    im2 = im2double(frames(:, :, :, i+1));
  else
    im1 = im2double(frames(:, :, i));
    im2 = im2double(frames(:, :, i+1));
  end
  [u v w2] = Coarse2FineTwoFrames(im1,im2,para);
  uv(:,:,1,i) = u';
  uv(:,:,2,i) = v';
end

% Writes the output
[pathstr, name, ext] = fileparts(inFile);
outFile = fullfile(outDir, [name '.hdf5']);
disp(sprintf('Saving flows to %s...', outFile));
if exist(outFile, 'file') ~= 0
  disp('Backing-up already existing file w/ the same name...');
  movefile(outFile, [outFile '~'], 'f');
end
h5create(outFile, '/uv', size(uv));
h5write(outFile, '/uv', uv);
h5writeatt(outFile, '/uv', 'method', 'SOR');
h5writeatt(outFile, '/uv', 'alpha', alpha);
h5writeatt(outFile, '/uv', 'ratio', ratio);
h5writeatt(outFile, '/uv', 'min_width', minWidth);
h5writeatt(outFile, '/uv', 'n_outer_fp_iterations', nOuterFPIterations);
h5writeatt(outFile, '/uv', 'n_inner_fp_iterations', nInnerFPIterations);
h5writeatt(outFile, '/uv', 'n_iterations', nIterations);
disp(sprintf('Done. Function ended.'));
