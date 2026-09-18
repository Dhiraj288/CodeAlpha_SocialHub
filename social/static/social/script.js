document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // DARK / LIGHT MODE
    // ==========================================

    const themeToggle = document.getElementById("theme-toggle");

    const savedTheme = localStorage.getItem("socialhub-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");

        if (themeToggle) {
            themeToggle.textContent = "☀️";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to light mode"
            );
        }
    } else {
        if (themeToggle) {
            themeToggle.textContent = "🌙";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to dark mode"
            );
        }
    }


    if (themeToggle) {

        themeToggle.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            const darkModeEnabled =
                document.body.classList.contains("dark-mode");

            if (darkModeEnabled) {

                localStorage.setItem(
                    "socialhub-theme",
                    "dark"
                );

                themeToggle.textContent = "☀️";

                themeToggle.setAttribute(
                    "aria-label",
                    "Switch to light mode"
                );

            } else {

                localStorage.setItem(
                    "socialhub-theme",
                    "light"
                );

                themeToggle.textContent = "🌙";

                themeToggle.setAttribute(
                    "aria-label",
                    "Switch to dark mode"
                );
            }
        });
    }


    // ==========================================
    // POST IMAGE PREVIEW
    // Used by Create Post + Edit Post
    // ==========================================

    const postImageInput =
        document.getElementById("post-image");

    const imagePreview =
        document.getElementById("image-preview");

    const imagePreviewContainer =
        document.getElementById(
            "image-preview-container"
        );

    const removePreviewButton =
        document.getElementById("remove-preview");


    if (
        postImageInput &&
        imagePreview &&
        imagePreviewContainer
    ) {

        postImageInput.addEventListener(
            "change",
            function () {

                const file = this.files[0];

                if (!file) {
                    hidePostPreview();
                    return;
                }


                // Make sure selected file is an image
                if (!file.type.startsWith("image/")) {

                    alert("Please select an image file.");

                    postImageInput.value = "";

                    hidePostPreview();

                    return;
                }


                const reader = new FileReader();


                reader.onload = function (event) {

                    imagePreview.src =
                        event.target.result;

                    imagePreviewContainer.style.display =
                        "block";
                };


                reader.readAsDataURL(file);
            }
        );
    }


    // REMOVE SELECTED POST IMAGE

    if (removePreviewButton) {

        removePreviewButton.addEventListener(
            "click",
            function () {

                if (postImageInput) {
                    postImageInput.value = "";
                }

                hidePostPreview();
            }
        );
    }


    function hidePostPreview() {

        if (imagePreview) {
            imagePreview.src = "";
        }

        if (imagePreviewContainer) {
            imagePreviewContainer.style.display =
                "none";
        }
    }


    // ==========================================
    // PROFILE PICTURE PREVIEW
    // ==========================================

    const profilePictureInput =
        document.getElementById(
            "profile-picture-input"
        );

    const profileImagePreview =
        document.getElementById(
            "profile-image-preview"
        );

    const currentProfilePicture =
        document.getElementById(
            "current-profile-picture"
        );

    const defaultProfilePicture =
        document.getElementById(
            "default-profile-picture"
        );


    if (
        profilePictureInput &&
        profileImagePreview
    ) {

        profilePictureInput.addEventListener(
            "change",
            function () {

                const file = this.files[0];

                if (!file) {

                    profileImagePreview.style.display =
                        "none";

                    profileImagePreview.src = "";

                    if (currentProfilePicture) {
                        currentProfilePicture.style.display =
                            "block";
                    }

                    if (defaultProfilePicture) {
                        defaultProfilePicture.style.display =
                            "flex";
                    }

                    return;
                }


                if (!file.type.startsWith("image/")) {

                    alert("Please select an image file.");

                    profilePictureInput.value = "";

                    return;
                }


                const reader = new FileReader();


                reader.onload = function (event) {

                    profileImagePreview.src =
                        event.target.result;

                    profileImagePreview.style.display =
                        "block";


                    // Hide current DP

                    if (currentProfilePicture) {

                        currentProfilePicture.style.display =
                            "none";
                    }


                    // Hide default icon

                    if (defaultProfilePicture) {

                        defaultProfilePicture.style.display =
                            "none";
                    }
                };


                reader.readAsDataURL(file);
            }
        );
    }

});