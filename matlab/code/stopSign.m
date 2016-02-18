%Author: Michael Glazer
%Date: 2/16/16
%Purpose: Proof of concept for stop sign recognition
%Process: resize an image to have a max row or col pixel size of 400
%       crop the image to remove the lower 25% where stop signs won't be
%       isolate the red colors in an image as much as possible
%       perform blob detection on resulting image for specific size range
%       visually analyze detected blobs and go from there

tic;

%delete any existing figures
close all

%--------------------READ IMAGE--------------------%

cd(fileparts(mfilename('fullpath')));
cd('..');
dataDir = fullfile('data/stop_signs');
outputDir = fullfile('output/stop_signs');
imageName = 'stop4.jpg';
name = imageName(1:end-4);
im = imread(fullfile(dataDir, imageName));

figure
imshow(im);
hold on
title('Original Image')
saveas(gcf, fullfile(outputDir, strcat(name, '_Original_Image.jpg')));
hold off

%--------------------RESIZE IMAGE--------------------%

%make longest edge 400
h = size(im,1);
w = size(im,2);
if h > w
    im = imresize(im, [400, w/(h/400)]);
    h = size(im,1);
    w = size(im,2);
    im = imcrop(im,[1 1 w h - (h/4)]);
else
    im = imresize(im, [h/(w/400), 400]);
    h = size(im,1);
    w = size(im,2);
    im = imcrop(im,[1 1 w h - (h/4)]);
end

%remove bottom 3rd of image
x = imcrop(im,[1 1 w 200]);

figure
imshow(im);
hold on
title('Resized Image')
saveas(gcf, fullfile(outputDir, strcat(name, '_Resized_Image.jpg')));
hold off

%--------------------THRESHOLD IMAGE--------------------%

for i = 1:size(im,1)
    for j = 1:size(im,2)
        if im(i,j,1) < 210 %|| im(i,j,3) + im(i,j,2) > 450
            im (i,j,:) = 0;
        end
    end
end
% im(:,:,2) = 0;
% im(:,:,3) = 0;

figure
imshow(im);
hold on
title('Thresholded Image')
saveas(gcf, fullfile(outputDir, strcat(name, '_Thresholded_Image.jpg')));
hold off

%--------------------DETECT BLOBS--------------------%
blobMeasurements = regionprops(im2bw(im), 'all');
numberOfBlobs = size(blobMeasurements, 1);

%remove all blobs with uncharacteristically low area
x = vertcat(blobMeasurements.Area);
x(x < 400) = 0;
boxes = vertcat(blobMeasurements.BoundingBox);
insert = [];

for i = 1:numberOfBlobs
    if x(i,1) ~= 0
        insert = [insert;boxes(i,:)];
    end
end
box = insertShape(im,'Rectangle',insert,'LineWidth',3);

%display all blobs that passed the tests
figure
% imshow(im);
hold on
imshow(box);
title('Chosen Blobs')
saveas(gcf, fullfile(outputDir, strcat(name, '_Chosen_Blobs.jpg')));
hold off

toc;