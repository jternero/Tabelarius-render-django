(function($) {

	"use strict";


})(jQuery);

document.addEventListener("DOMContentLoaded", function() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const uploadForm = document.getElementById("upload-form");
    const feedback = document.getElementById("upload-feedback");

    dropZone.addEventListener("click", () => fileInput.click());
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    });
    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
        fileInput.files = e.dataTransfer.files;
    });

    uploadForm.addEventListener("submit", function(e) {
        e.preventDefault();
        let formData = new FormData(uploadForm);
        fetch("/face_upload/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                feedback.innerHTML = `<p style='color: red;'>${data.error}</p>`;
            } else {
                feedback.innerHTML = `<p style='color: green;'>${data.success}</p>`;
            }
        })
        .catch(error => console.error("Error en la subida:", error));
    });
});

$(document).ready(function () {
    $("#upload-form").submit(function (e) {
        e.preventDefault();

        let formData = new FormData(this);

        $.ajax({
            url: "{% url 'face_upload' %}",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            },
            success: function (response) {
                $("#upload-feedback").html('<div class="alert alert-success">Archivos subidos con éxito.</div>');
            },
            error: function (xhr) {
                $("#upload-feedback").html('<div class="alert alert-danger">Error al subir los archivos.</div>');
            }
        });
    });
});
