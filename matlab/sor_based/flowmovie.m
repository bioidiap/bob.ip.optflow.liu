function [] = flowmovie(inFile, outDir)

% flowmovie(inFile, outDir)
%
% Computes the flow between every two successive frames of the given input
% movie file and stores the computed flow as .hdf5 to the output directory.
%
% This function is based on the original work from Murali M. Chakka and leads
% to *exact* the same results as his hold implementation.
%
% Improved by Andre Anjos <andre.anjos@idiap.ch>
% Thu 15 Nov 2012 16:55:36 CET

addpath('mex');

disp(sprintf('Loading contents of %s...', inFile));
videoObject = mmreader(inFile);
frames = read(videoObject) ; % frames will be uint8 at this point
disp(sprintf('Loaded %d frames.', videoObject.NumberOfFrames));

% Set optical flow parameters (see Coarse2FineTwoFrames.m for the definition of
% the parameters)
alpha = 1.0;
ratio = 0.5;
minWidth = 40;
nOuterFPIterations = 4;
nInnerFPIterations = 1;
nIterations = 20;

para = [alpha,ratio,minWidth,nOuterFPIterations,nInnerFPIterations,nIterations];

for i = 1 : a.NumberOfFrames-1
  disp(sprintf(' * Evaluating flow between frames #%d -> #%d', i, i+1));
  im1 = im2double(frames(:, :, :, i));
  im2 = im2double(frames(:, :, :, i+1));
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
h5create(outFile, '/frames', size(frames(:,:,:));
h5writeatt(outFile, '/uv', 'method', 'SOR');
h5writeatt(outFile, '/uv', 'alpha', alpha);
h5writeatt(outFile, '/uv', 'ratio', ratio);
h5writeatt(outFile, '/uv', 'min_width', minWidth);
h5writeatt(outFile, '/uv', 'n_outer_fp_iterations', nOuterFPIterations);
h5writeatt(outFile, '/uv', 'n_inner_fp_iterations', nInnerFPIterations);
h5writeatt(outFile, '/uv', 'n_iterations', nIterations);
disp(sprintf('Done. Function ended.'));
