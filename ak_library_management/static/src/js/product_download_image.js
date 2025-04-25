function downloadSelectedImages() {
    let form = document.getElementById("imageSelectionForm");
    let formData = new FormData(form);
    let selectedImages = [];

    formData.getAll("selected_images").forEach((value) => {
        selectedImages.push(value);
    });

    if (selectedImages.length === 0) {
        alert("Please select at least one image.");
        return;
    }

    let progressBar = document.getElementById("progressBar");
    let progressBarContainer = document.getElementById("progressBarContainer");
    progressBarContainer.style.display = "block";
    progressBar.style.width = "10%";

    fetch("/process_selected_images", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_id: formData.get("product_id"),
            selected_images: selectedImages,
        }),
    })
        .then(response => response.json())
        .then(data => {
            progressBar.style.width = "70%";

            if (data.error) {
                alert("Error: " + data.error);
                progressBarContainer.style.display = "none";
                return;
            }

            // Convert base64 to blob and trigger download
            let zipBlob = new Blob([new Uint8Array(atob(data.zip_file).split("").map(c => c.charCodeAt(0)))], { type: "application/zip" });
            let link = document.createElement("a");
            link.href = URL.createObjectURL(zipBlob);
            link.download = data.file_name;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            progressBar.style.width = "100%";
            setTimeout(() => { progressBarContainer.style.display = "none"; }, 2000);
        })
        .catch(error => {
            alert("An error occurred.");
            console.error(error);
            progressBarContainer.style.display = "none";
        });
}
