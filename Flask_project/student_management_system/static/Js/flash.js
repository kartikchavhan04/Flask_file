document.addEventListener("DOMContentLoaded", function () {

    const popups =
        document.querySelectorAll(".flash-popup");


    popups.forEach(function (popup) {


        // Close button

        const closeButton =
            popup.querySelector(".flash-close");


        closeButton.addEventListener("click", function () {

            closePopup(popup);

        });


        // Automatically close after 3 seconds

        setTimeout(function () {

            closePopup(popup);

        }, 3000);

    });


    function closePopup(popup) {

        popup.style.opacity = "0";

        popup.style.transform = "translateX(100px)";


        setTimeout(function () {

            popup.remove();

        }, 400);

    }

});