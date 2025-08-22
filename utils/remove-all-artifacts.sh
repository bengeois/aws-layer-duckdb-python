#!/bin/bash

# Avertissement: Ceci est une action destructive et irréversible.
# Définis le propriétaire et le nom du dépôt
OWNER="bengeois"
REPO="aws-layer-duckdb-python"

# Liste toutes les exécutions de workflow pour le dépôt
echo "Listing all workflow runs for $OWNER/$REPO..."
RUNS=$(gh run list --repo $OWNER/$REPO --json databaseId --jq '.[].databaseId')

# Pour chaque exécution, liste et supprime ses artifacts
for run_id in $RUNS; do
    echo "Processing workflow run ID: $run_id"
    
    # Liste les artifacts de cette exécution
    ARTIFACTS=$(gh api "repos/$OWNER/$REPO/actions/runs/$run_id/artifacts" --jq '.artifacts')

    # Si des artifacts existent, les supprimer un par un
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