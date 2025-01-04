import json

def update_file_paths(json_file_path, output_file_path):
    """
    Update the file paths in the JSON file:
    - Replace backslashes with forward slashes.
    - Add '../' before 'corpus'.
    
    Args:
        json_file_path (str): Path to the input JSON file.
        output_file_path (str): Path to save the updated JSON file.
    """
    try:
        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as file:
            documents = json.load(file)

        # Update the file paths
        for doc in documents:
            if "file_path" in doc:
                original_path = doc["file_path"]
                updated_path = "../" + original_path.replace("\\", "/")
                doc["file_path"] = updated_path

        # Save the updated JSON data
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(documents, file, indent=4, ensure_ascii=False)

        print(f"File paths updated and saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_json = "all_documents.json"  # Input JSON file
output_json = "updated_all_documents.json"  # Output JSON file with updated paths
update_file_paths(input_json, output_json)
