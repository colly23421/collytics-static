document.addEventListener("DOMContentLoaded", function() {
    const menuTrigger = document.getElementById("menuTrigger");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const menuOverlay = document.getElementById("menuOverlay");
    const closeMenu = document.getElementById("closeMenu");
    const navbar = document.querySelector(".navbar");
    
    // Toggle menu
    function toggleMenu() {
        menuTrigger.classList.toggle("active");
        dropdownMenu.classList.toggle("active");
        menuOverlay.classList.toggle("active");
    }
    
    if(menuTrigger) menuTrigger.addEventListener("click", toggleMenu);
    if(closeMenu) closeMenu.addEventListener("click", toggleMenu);
    if(menuOverlay) menuOverlay.addEventListener("click", toggleMenu);
    
    // ESC key to close
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape" && dropdownMenu && dropdownMenu.classList.contains("active")) {
            toggleMenu();
        }
    });
    
    // Hide navbar on scroll down, show on scroll up
    let lastScrollTop = 0;
    window.addEventListener("scroll", function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down - hide navbar
            navbar.style.transform = "translateY(-100%)";
        } else {
            // Scrolling up - show navbar
            navbar.style.transform = "translateY(0)";
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
});
