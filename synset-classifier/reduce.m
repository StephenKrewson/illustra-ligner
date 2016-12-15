% trying out some different viz of the 2048-dim that inception gives back
load('inception.mat');

[N,n] = size(matrix);

no_dims = round(intrinsic_dim(matrix, 'MLE'));
disp(['MLE estimate of intrinsic dimensionality: ' num2str(no_dims)]);

% WOW--MLE says it's 13 dims; best results from PCA on first 2 and then
% laplacian eigenmaps!!!!!!!! (it preserves all data points)
[mappedX, mapping] = compute_mapping(matrix, 'PCA', no_dims);	
figure, scatter3(mappedX(:,1), mappedX(:,2), mappedX(:,3)); title('Result of PCA (3 components)');

[mappedX, mapping] = compute_mapping(matrix, 'Laplacian', no_dims, 7);	
figure, scatter3(mappedX(:,1), mappedX(:,2), mappedX(:,3)); title('Result of Laplacian Eigenmaps'); drawnow

% Constrain to first three principal components, get the pointwise
% distances and then do agglomerative single link clustering (cf. with
% average, which actuall does better)
X = mappedX(:,1:3);
eucD = pdist2(X,X);
clustTreeEuc = linkage(eucD,'average');
cophenet(clustTreeEuc,eucD)

[h,nodes] = dendrogram(clustTreeEuc,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];

% Get the images; remember to offset by 2 to account for dir symlinks
% we also want to make them all the same size
location = '../img/thumbnails/';
imagelist = dir(location);

% https://www.mathworks.com/help/stats/examples/cluster-analysis.html
% 1) create montages (cutoff depends on average vs. single-link)
hidx = cluster(clustTreeEuc,'criterion','distance','cutoff',0.19);
for i = 1:no_dims
    clust = find(hidx==i);
    filenames = {imagelist(clust+2).name};
    absopaths = strcat(location,filenames);
    figure, imdisp(absopaths); title(num2str(i));
end

% 2) create 3-D scatterplot of the laplacian eigenmap clusters; use two
% loops since otherwise the figure handles would get crazy
for i = 1:no_dims
    clust = find(hidx==i);
    scatter3(X(clust,1),X(clust,2),X(clust,3));title('Clusters');
    hold on
end
hold off
grid on