// let viz;

// //Add Share Link to Tableau Public in here
// const url = "https://public.tableau.com/views/AlarmsInIsrael/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link";

// //https://public.tableau.com/shared/5ZJRNMD4T?:display_count=n&:origin=viz_share_link

// const vizContainer = document.getElementById('vizContainer');
// const options = {
//     hideTabs: true,
//     height: 1000,
//     width: 1200,
//     onFirstInteraction: function() {
//         workbook = viz.getWorkbook();
//         activeSheet = workbook.getActiveSheet();
//         console.log("My dashboard is interactive");
//     }
// };

// //create a function to generate the viz element
// function initViz() {
//     console.log('Executing the initViz function!');
//     viz = new tableau.Viz(vizContainer, url, options);
// }

// // run the initViz function when the page loads
// document.addEventListener("DOMContentLoaded", initViz);

let viz1, viz2;

// Add the URLs for your Tableau Public dashboards
const url1 = "https://public.tableau.com/views/AlarmsInIsrael/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link";
const url2 = "https://public.tableau.com/shared/5ZJRNMD4T?:display_count=n&:origin=viz_share_link";

// Configuration options for the Tableau visualizations
const options = {
    hideTabs: true,
    height: 1000,
    width: 1200,
    onFirstInteraction: function () {
        console.log("Dashboard is interactive");
    }
};

// Function to initialize the first Tableau dashboard
function initViz1() {
    const vizContainer1 = document.getElementById('vizContainer1');
    if (!viz1) { // Prevent initializing multiple times
        viz1 = new tableau.Viz(vizContainer1, url1, options);
    }
}

// Function to initialize the second Tableau dashboard
function initViz2() {
    const vizContainer2 = document.getElementById('vizContainer2');
    if (!viz2) { // Prevent initializing multiple times
        viz2 = new tableau.Viz(vizContainer2, url2, options);
    }
}

// Run initialization functions when the tab is clicked
document.addEventListener("DOMContentLoaded", () => {
    initViz1(); // Initialize the first dashboard on page load
});
