#!/bin/bash

# WARNING: This is a destructive and irreversible action.
# Define the owner and repository name
OWNER="bengeois"
REPO="aws-layer-duckdb-python"

# List all workflow runs for the repository
echo "Listing all workflow runs for $OWNER/$REPO..."
RUNS=$(gh run list --repo $OWNER/$REPO --json databaseId --jq '.[].databaseId')

# For each run, list and delete its artifacts
for run_id in $RUNS; do
    echo "Processing workflow run ID: $run_id"

    # List the artifacts for this run
    ARTIFACTS=$(gh api "repos/$OWNER/$REPO/actions/runs/$run_id/artifacts" --jq '.artifacts')

    # If artifacts exist, delete them one by one
    if [[ $(echo $ARTIFACTS | jq 'length') -gt 0 ]]; then
        echo "  Found artifacts. Deleting them..."
        ARTIFACT_IDS=$(echo $ARTIFACTS | jq '.[].id')
        
        for artifact_id in $ARTIFACT_IDS; do
            echo "    Deleting artifact ID: $artifact_id"
            gh api --method DELETE "repos/$OWNER/$REPO/actions/artifacts/$artifact_id" > /dev/null
        done
    else
        echo "  No artifacts found for this run."
    fi
done

echo "All artifacts have been processed."