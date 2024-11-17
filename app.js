

// Array of Tableau dashboard URLs
const dashboardURLs = [
    "https://public.tableau.com/views/AlarmsIsrael1/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link",
    "https://public.tableau.com/views/AlarmsIsrael2/AlarmsinMonths?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link",
    "https://public.tableau.com/views/AlarmsIsrael3/CitiesDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
];

const dashboardNames = [
    "By Hour,Minutes,Hours",
    "By Date",
    "By City"
];

vizContainer.innerHTML = `
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; height: 100%;">
        <div id="vizContainer${index}" class="viz"></div>
    </div>
`;


// Options for all dashboards
const options = {
    hideTabs: true,
    height: 1200,
    width: 1600,
    onFirstInteraction: function () {
        console.log("Dashboard is interactive");
    }
};

// Array to hold initialized dashboard instances
let vizInstances = Array(dashboardURLs.length).fill(null);

// Function to initialize a dashboard only when needed
function initViz(index) {
    if (!vizInstances[index]) {
        const vizContainer = document.getElementById('vizContainer' + index);
        vizInstances[index] = new tableau.Viz(vizContainer, dashboardURLs[index], options);
    }
}

// Function to dynamically set up tabs and containers
function setupDashboardTabs() {
    const tabContainer = document.getElementById("tabContainer");
    const dashboardContainer = document.getElementById("dashboardContainer");

    dashboardURLs.forEach((url, index) => {
        // Create a new tab button
        const tabButton = document.createElement("button");
        tabButton.className = "tablinks";
        //tabButton.innerText = `Dashboards ${index + 1}`;
        tabButton.innerText = dashboardNames[index];
        tabButton.onclick = (event) => {
            openDashboard(event, index);
            initViz(index);
        };
        tabContainer.appendChild(tabButton);

        // Create a new dashboard container
        const vizContainer = document.createElement("div");
        vizContainer.className = "dashboard-container";
        vizContainer.id = "Dashboard" + index;
        vizContainer.innerHTML = `<div id="vizContainer${index}" class="viz"></div>`;
        dashboardContainer.appendChild(vizContainer);
    });
}

// Initialize tabs and containers on page load
document.addEventListener("DOMContentLoaded", setupDashboardTabs);