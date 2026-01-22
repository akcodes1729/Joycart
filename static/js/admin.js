

let users = [];
let filteredUsers = [];
let currentPage = 1;
let pageSize = 8;
let currentSortKey = "id";
let sortAsc = true;

async function fetchUsers() {
  const res = await fetch("/admin/users", {
    credentials: "include" 
  });
  users = await res.json();
  applyFilters();
}

function applyFilters() {
  const roleFilter = document.getElementById("filterRole").value;
  const blockedFilter = document.getElementById("filterBlocked").value;

  filteredUsers = users.filter(u => {
    if (roleFilter !== "all" && u.role !== roleFilter) return false;
    if (blockedFilter === "blocked" && !u.is_blocked) return false;
    if (blockedFilter === "active" && u.is_blocked) return false;
    return true;
  });

  sortUsers(currentSortKey);
}

function sortBy(key) {
  sortAsc = currentSortKey === key ? !sortAsc : true;
  currentSortKey = key;
  sortUsers(key);
}

function sortUsers(key) {
  filteredUsers.sort((a, b) => {
    if (a[key] < b[key]) return sortAsc ? -1 : 1;
    if (a[key] > b[key]) return sortAsc ? 1 : -1;
    return 0;
  });
  renderTable();
}

function renderTable() {
  const table = document.getElementById("usersTable");
  table.innerHTML = "";

  const start = (currentPage - 1) * pageSize;
  const pageUsers = filteredUsers.slice(start, start + pageSize);

  pageUsers.forEach(u => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${u.id}</td>
      <td>${u.username}</td>
      <td>${u.email}</td>
      <td>${u.role}</td>
      <td>${u.is_blocked ? "Yes" : "No"}</td>
      <td>
        ${u.is_blocked
          ? `<button class="btn btn-success" onclick="unblockUser(${u.id})">Unblock</button>`
          : `<button class="btn btn-danger" onclick="blockUser(${u.id})">Block</button>`
        }
        ${u.role !== "admin"
          ? `<button class="btn btn-warning" onclick="makeAdmin(${u.id})">Make Admin</button>`
          : ""
        }
      </td>
    `;

    table.appendChild(row);
  });

  document.getElementById("pageInfo").innerText =
    `Page ${currentPage} of ${Math.ceil(filteredUsers.length / pageSize)}`;
}

function nextPage() {
  if (currentPage * pageSize < filteredUsers.length) {
    currentPage++;
    renderTable();
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    renderTable();
  }
}

async function blockUser(id) {
  await fetch(`/admin/users/${id}/block`, { method: "PUT", credentials: "include" });
  fetchUsers();
}

async function unblockUser(id) {
  await fetch(`/admin/users/${id}/unblock`, { method: "PUT", credentials: "include" });
  fetchUsers();
}

async function makeAdmin(id) {
  if (!confirm("Promote this user to admin?")) return;
  await fetch(`/admin/users/${id}/make-admin`, { method: "PUT", credentials: "include" });
  fetchUsers();
}

document.getElementById("filterRole").onchange = applyFilters;
document.getElementById("filterBlocked").onchange = applyFilters;

fetchUsers();
