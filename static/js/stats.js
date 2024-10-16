const ctx = document.getElementById("myChart");
const renderChart = (data, labels) => {
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last six months expenses",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
          borderWidth: 1,
          borderWidth: 1,
          borderWidth: 1,
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      responsive: false, // Disable responsive resizing
      maintainAspectRatio: false, // Prevent Chart.js from maintaining aspect ratio
      plugins: {
        title: {
          display: true,
          text: "Expenses per category",
          font: {
            size: 16,
            weight: "bold",
          },
        },
      },
      // scales: {
      //   y: {
      //     beginAtZero: true, // Ensure the y-axis starts from 0
      //   },
      // },
    },
  });
};

const getChartData = () => {
  console.log("fetching...");
  fetch("/expense-category-summary/")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);

      const labels = Object.keys(results.expense_category_data);
      const data = Object.values(results.expense_category_data);

      renderChart(data, labels);
    })
    .catch((error) => console.error("Error fetching chart data:", error));
};

document.onload = getChartData();
