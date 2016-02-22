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
imageName = 'stop11.jpg';
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
%crop the bottom 4th of the image
if h > w
    im = imresize(im, [400, w/(h/400)]);
    h = size(im,1);
    w = size(im,2);
    im = imcrop(im,[1 1 w h - (h/4)]);  %the crop
else
    im = imresize(im, [h/(w/400), 400]);
    h = size(im,1);
    w = size(im,2);
    im = imcrop(im,[1 1 w h - (h/4)]);
end


figure
imshow(im);
hold on
title('Resized Image')
saveas(gcf, fullfile(outputDir, strcat(name, '_Resized_Image.jpg')));
hold off

%--------------------THRESHOLD IMAGE--------------------%

for i = 1:size(im,1)
    for j = 1:size(im,2)
        if double(im(i,j,1)) / (double(im(i,j,2)) + double(im(i,j,3))) < 1.1 % im(i,j,3) + im(i,j,2) > 450
            im (i,j,:) = 0; %make the pixel black, if its not red enough
        end
    end
end

im(im > 0) = 255;

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
choices = ones(numberOfBlobs,1);
x = vertcat(blobMeasurements.Area);
y = vertcat(blobMeasurements.FilledArea);
z = vertcat(blobMeasurements.ConvexArea);
k = cell(numberOfBlobs,1);
for i = 1:numberOfBlobs
    k{i,1} = blobMeasurements(i).ConvexImage;
end

choices(x < 400 | y < 1000) = 0;

%divide the longest dimension of the region by 5
%if the difference between the convex image dimensions are greater than it,
%remove it from the list of possibilities (looking for ~square img)
for i = 1:numberOfBlobs
    if choices(i,1) ~= 0
        maxSize = max(size(cell2mat(k(i,1)),1), size(cell2mat(k(i,1)),2))/5;
        if abs(size(cell2mat(k(i,1)),1) - size(cell2mat(k(i,1)),2)) > maxSize
            choices(i,1) = 0;
        end
    end
end

% for i = 1:numberOfBlobs
%     if abs(y(i,1) - z(i,1)) > 500
%         x(i,1) = 0;
%     end
% end


boxes = vertcat(blobMeasurements.BoundingBox);
insert = [];
chosenBlobs = [];

for i = 1:numberOfBlobs
    if choices(i,1) ~= 0 %&& i ~= 2 && i ~= 3
        insert = [insert;boxes(i,:)];
        chosenBlobs = [chosenBlobs,i];
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


fprintf('Chosen Blobs = %f\n', chosenBlobs); 

toc;