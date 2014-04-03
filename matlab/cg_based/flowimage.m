function flowimage(indir, sample, outdir)

% flowimage(indir, sample, outdir)
%
% Runs the optical flow estimator machinery on the input files and output the
% results in the HDF5 file named by output.
%
% Andre Anjos <andre.anjos@idiap.ch>
% Fri 09 Nov 2012 13:11:38 CET

addpath('mex');

% load the two frames
file1 = fullfile(indir, [sample '1.png']);
disp(sprintf('Loading image %s...', file1));
im1 = im2double(imread(file1));
file2 = fullfile(indir, [sample '2.png']);
disp(sprintf('Loading image %s...', file2));
im2 = im2double(imread(file2));

alpha = 0.02;
ratio = 0.75;
minWidth = 30;
nOuterFPIterations = 20;
nInnerFPIterations = 1;
nIterations = 50;

para = [alpha,ratio,minWidth,nOuterFPIterations,nInnerFPIterations,nIterations];

disp('Estimating flow...');
drawnow('update'); %flush stdout
[vx,vy,warpI2] = Coarse2FineTwoFrames(im1,im2,para);

f(:,:,1) = vx';
f(:,:,2) = vy';

% Writes the output
output = fullfile(outdir, [sample '.hdf5']);
disp(sprintf('Saving flow to %s...', output));
if exist(output, 'file') ~= 0
  disp('Backing-up already existing file w/ the same name...');
  movefile(output, [output '~'], 'f');
end
h5create(output, '/uv', size(f));
h5write(output, '/uv', f);
h5writeatt(output, '/uv', 'method', 'CG');
h5writeatt(output, '/uv', 'alpha', alpha);
h5writeatt(output, '/uv', 'ratio', ratio);
h5writeatt(output, '/uv', 'min_width', minWidth);
h5writeatt(output, '/uv', 'n_outer_fp_iterations', nOuterFPIterations);
h5writeatt(output, '/uv', 'n_inner_fp_iterations', nInnerFPIterations);
h5writeatt(output, '/uv', 'n_iterations', nIterations);
