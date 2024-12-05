// document.addEventListener("DOMContentLoaded", () => {
//     const menuLinks = document.querySelectorAll('a[data-page]');
//     const mainContent = document.getElementById('main-content');

//     // Attach click event listeners to menu items
//     menuLinks.forEach(link => {
//         link.addEventListener('click', async (e) => {
//             e.preventDefault();

//             const page = e.target.getAttribute('data-page');
//             await loadPage(page);
//         });
//     });

//     async function loadPage(page) {
//         try {
//             // Fetch the HTML content of the selected page
//             const response = await fetch(`${page}.html`);
//             const content = await response.text();

//             // Replace the main content
//             mainContent.innerHTML = content;
//         } catch (error) {
//             mainContent.innerHTML = "<p>Error loading page.</p>";
//             console.error(error);
//         }
//     }
// });
