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
imageName = 'stop3.jpg';
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
% 
% if strcmpi(class(im), 'uint8')
%     % Flag for 256 gray levels.
%     eightBit = true;
% else
%     eightBit = false;
% end
% 
% redBand = im(:,:,1); 
% greenBand = im(:,:,2); 
% blueBand = im(:,:,3);
% 
% imshow(redBand, []);
% 
% redThresholdLow = graythresh(redBand);
% redThresholdHigh = 255;
% greenThresholdLow = 0;
% greenThresholdHigh = graythresh(greenBand);
% blueThresholdLow = 0;
% blueThresholdHigh = graythresh(blueBand);
% if eightBit
%     redThresholdLow = uint8(redThresholdLow * 255);
%     greenThresholdHigh = uint8(greenThresholdHigh * 255);
%     blueThresholdHigh = uint8(blueThresholdHigh * 255);
% end
% 
% redMask = (redBand >= redThresholdLow) & (redBand <= redThresholdHigh);
% greenMask = (greenBand >= greenThresholdLow) & (greenBand <= greenThresholdHigh);
% blueMask = (blueBand >= blueThresholdLow) & (blueBand <= blueThresholdHigh);
% 
% % Display the thresholded binary images.
% 	fontSize = 16;
% 	subplot(3, 4, 10);
% 	imshow(redMask, []);
% 	title('Is-Red Mask', 'FontSize', fontSize);
% 	subplot(3, 4, 11);
% 	imshow(greenMask, []);
% 	title('Is-Not-Green Mask', 'FontSize', fontSize);
% 	subplot(3, 4, 12);
% 	imshow(blueMask, []);
% 	title('Is-Not-Blue Mask', 'FontSize', fontSize);
% 	% Combine the masks to find where all 3 are "true."
% 	% Then we will have the mask of only the red parts of the image.
% 	redObjectsMask = uint8(redMask & greenMask & blueMask);
% 	subplot(3, 4, 9);
% 	imshow(redObjectsMask, []);
% 	caption = sprintf('Mask of Only\nThe Red Objects');
% 	title(caption, 'FontSize', fontSize);
% fprintf('RGB:%f %f %f', redThresholdLow, greenThresholdHigh, blueThresholdHigh);
% 
% 
% 
% 
% 
% imshow(redMask, []);
% 
% redObjectsMask = uint8(redMask & greenMask & blueMask);
% 
% imshow(redObjectsMask, []);
% 
% smallestAcceptableArea = 100;
% redObjectsMask = uint8(bwareaopen(redObjectsMask, smallestAcceptableArea));
% 
% imshow(redObjectsMask, []);
% 
% structuringElement = strel('disk', 4);
% redObjectsMask = imclose(redObjectsMask, structuringElement);
% 
% redObjectsMask = uint8(imfill(redObjectsMask, 'holes'));
% 
% redObjectsMask = cast(redObjectsMask, class(redBand)); 
% 
% imshow(redObjectsMask, []);
% 
% maskedImageR = redObjectsMask .* redBand;
% maskedImageG = redObjectsMask .* greenBand;
% maskedImageB = redObjectsMask .* blueBand;
% 
% imshow(maskedImageR);
% title('Masked Red Image');
% 




for i = 1:size(im,1)
    for j = 1:size(im,2)
        if double(im(i,j,1)) / (double(im(i,j,2)) + double(im(i,j,3))) < 1.0001 % im(i,j,3) + im(i,j,2) > 450
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
choices = ones(numberOfBlobs,1);
x = vertcat(blobMeasurements.Area);
y = vertcat(blobMeasurements.FilledArea);
z = vertcat(blobMeasurements.ConvexArea);
k = cell(numberOfBlobs,1);
for i = 1:numberOfBlobs
    k{i,1} = blobMeasurements(i).ConvexImage;
end

choices(x < 400 | abs(y-z) > 500 | y < 3000) = 0;

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