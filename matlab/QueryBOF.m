clear all; close all; clc; 

%% this section loads target images and creates the bag of features, 
%latter of which is only done once 
setDir = fullfile('./book_1');
imgs = imageDatastore(setDir, 'IncludeSubfolders', true,'LabelSource','foldernames')
%index = indexImages(imageSet(imgs.Files), 'SaveFeatureLocations', false);

%% display target images in order
helperDisplayImageMontage(imgs.Files)
print('book1' ,'-dpng')

%% load trained BOF, index

%data = load('book_1_2_BOF.mat');
%bag = data.bag

data = load('book1_index.mat')
index = data.index

figure
plot(sort(index.WordFrequency))
print('book1_wordfrequency', '-dpng')

%% query all images in testing file 
rng(2423)


qDir = fullfile('../testing-images/');
testImages = imageDatastore(qDir, 'IncludeSubfolders', true);
% select a small subsample size k of the full testing images 
k = 15;
qImages = randsample(testImages.Files, k)
qImages(1)

allScores = []


for i = 1:k
    qPath = imageDatastore(qImages(i))
    qImage = readimage(qPath,1);
    [imageIDs, scores] = retrieveImages(qImage, index)
    allScores = [allScores ; scores]
   
    imshow(qImage)
    fname=sprintf('book1_image%d_1',i);
    print(fname,'-dpng');
    helperDisplayImageMontage(imgs.Files(imageIDs))
    fname=sprintf('book1_image%d_2',i);
    print(fname,'-dpng');
    %% plot the similarities by score
    figure;
    error = std(scores)
    n = size(scores,1)
    error = repmat(error,n,1)
    errorbar(imageIDs,scores,error,'.')
    hold on;
    % add red marker to max
    scatter(imageIDs(1),scores(1),25,'r*')
    xlabel('target image id');
    ylabel('similarity')
    fname=sprintf('book1_image%d_3',i);
    print(fname,'-dpng');
    hold off;
end

%% hardcoded labels, for seed 2423 could be redone to be loaded from a table
%correct groups book1, done by hand
C = [11,8,0,9,0,6,0,5,1,11,12,0,0,8]
% chosen labels, done by hand
L = [11,8,10,12,12,12,12,5,1,11,12,4,12,8]

% correct groups book2
%C = [11,8,0,0,12,0,6,0,5,1,10,12,0,0,7]
%L = [11,8,10,12,12,12,2,4,5,1,10,12,4,12,7]


%% visualization  
confusion = confusionmat(C,L)
imagesc(confusion)
xlabel('assigned label');
ylabel('correct class')
% accuracy
accuracy = trace(confusion)/15
% without non-classified images
accuracy2 = trace(confusion)/8


