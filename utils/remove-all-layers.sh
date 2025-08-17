#!/bin/bash

# List all regions
REGIONS=$(aws ec2 describe-regions --all-regions --query "Regions[].RegionName" --output text --profile duckdb-layers)

for REGION in $REGIONS; do
  echo "Processing region: $REGION"

  # List layers in the region
  LAYERS=$(aws lambda list-layers --region $REGION --query "Layers[].LayerName" --output text --profile duckdb-layers)

  for LAYER in $LAYERS; do
    echo "  Processing layer: $LAYER"

    # List all versions of the layer
    VERSIONS=$(aws lambda list-layer-versions --layer-name $LAYER --region $REGION --query "LayerVersions[].Version" --output text --profile duckdb-layers)

    for VERSION in $VERSIONS; do
      echo "    Deleting layer version: $LAYER, version $VERSION"
      aws lambda delete-layer-version --layer-name $LAYER --version-number $VERSION --region $REGION --profile duckdb-layers
    done
  done
done