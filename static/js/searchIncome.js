// const searchField = document.querySelector("#searchField");
// const tableOutput = document.querySelector(".table-output");
// const appTable = document.querySelector(".app-table");
// const paginationContainer = document.querySelector(".pagination-container");
// const tableBody = document.querySelector(".table-body");

// // Initially hide the output table
// tableOutput.style.display = "none";

// searchField.addEventListener("keyup", (e) => {
//   const searchValue = e.target.value;

//   // Only perform the search if there is some input
//   if (searchValue.trim().length > 0) {
//     paginationContainer.style.display = "none"; // Hide pagination
//     tableBody.innerHTML = ""; // Clear previous results

//     fetch("/income/search-income/", {
//       body: JSON.stringify({ searchText: searchValue }),
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json", // Specify the content type
//         "X-CSRFToken": getCookie("csrftoken"), // Add CSRF token if necessary
//       },
//     })
//       .then((res) => {
//         if (!res.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return res.json(); // Parse JSON
//       })
//       .then((data) => {
//         console.log("Received data:", data); // Log the data

//         appTable.style.display = "none"; // Hide main table
//         tableOutput.style.display = "block"; // Show output table

//         // Check if the data array is empty
//         if (data.length === 0) {
//           tableBody.innerHTML = `
//             <tr>
//               <td colspan='4'>
//                 <div class="alert alert-warning" role="alert">
//                   No results found
//                 </div>
//               </td>
//             </tr>`;
//         } else {
//           data.forEach((income) => {
//             tableBody.innerHTML += `
//               <tr>
//                 <td>${income.amount}</td>
//                 <td>${income.source}</td>
//                 <td>${income.description}</td>
//                 <td>${new Date(income.date).toLocaleDateString()}</td>
//               </tr>`;
//           });
//         }
//       })
//       .catch((error) => {
//         console.error("Error fetching data:", error);
//         tableBody.innerHTML = "<tr><td colspan='4'>An error occurred while fetching data. Please try again.</td></tr>";
//       });
//   } else {
//     appTable.style.display = "block"; // Show main table
//     paginationContainer.style.display = "block"; // Show pagination
//     tableOutput.style.display = "none"; // Hide output table
//   }
// });

// const searchField = document.querySelector("#searchField");
// const tableOutput = document.querySelector(".table-output");
// const appTable = document.querySelector(".app-table");
// const paginationContainer = document.querySelector(".pagination-container");
// const tableBody = document.querySelector(".table-body");

// tableOutput.style.display = "none";

// searchField.addEventListener("keyup", (e) => {
//   const searchValue = e.target.value;

//   if (searchValue.trim().length > 0) {
//     paginationContainer.style.display = "none";
//     tableBody.innerHTML = "";

//     fetch("/income/search-income/", {
//       body: JSON.stringify({ searchText: searchValue }),
//       method: "POST",
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         console.log("data", data);
//         appTable.style.display = "none";
//         tableOutput.style.display = "block";

//         if (data.length === 0) {
//           tableOutput.innerHTML = `
//                     <tr>
//                         <td colspan='4'>
//                             <div class="alert alert-warning" role="alert">
//                                 No results found
//                             </div>
//                         </td>
//                     </tr>`;
//         } else {
//           data.forEach((income) => {
//             tableBody.innerHTML += `
//                     <tr>
//                       <td>${income.amount}</td>
//                       <td>${income.source}</td>
//                       <td>${income.description}</td>
//                       <td>${income.date}</td>
//                     </tr>`;
//           });
//         }
//       });
//   } else {
//     appTable.style.display = "block";
//     paginationContainer.style.display = "block";
//     tableOutput.style.display = "none";
//   }
// });


const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");

// Initially hide the output table
tableOutput.style.display = "none";

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none"; // Hide pagination
        tableBody.innerHTML = ""; // Clear previous results

        fetch("/income/search-income/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
            headers: {
                "Content-Type": "application/json", // Specify the content type
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
            },
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Network response was not ok");
                }
                return res.json(); // Parse the JSON response
            })
            .then((data) => {
                console.log("data", data);
                appTable.style.display = "none"; // Hide main table
                tableOutput.style.display = "block"; // Show output table

                // Check if there are any results
                if (data.length === 0) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan='4'>
                                <div class="alert alert-danger" role="alert">
                                    No results found
                                </div>
                            </td>
                        </tr>`;
                } else {
                    // Populate the table with search results
                    data.forEach((income) => {
                        tableBody.innerHTML += `
                            <tr>
                                <td>${income.amount}</td>
                                <td>${income.source}</td>
                                <td>${income.description}</td>
                                <td>${income.date}</td>
                            </tr>`;
                    });
                }
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                // Optionally display an error message to the user
                tableBody.innerHTML = `
                    <tr>
                        <td colspan='4'>
                            <div class="alert alert-danger" role="alert">
                                An error occurred while fetching data. Please try again.
                            </div>
                        </td>
                    </tr>`;
            });
    } else {
        appTable.style.display = "block"; // Show main table
        paginationContainer.style.display = "block"; // Show pagination
        tableOutput.style.display = "none"; // Hide output table
    }
});
