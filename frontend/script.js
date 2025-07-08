document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');
  const errorMessage = document.getElementById('error-message');

  if (loginForm) {
    loginForm.addEventListener('submit', async function (e) {
      e.preventDefault();

      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!username || !password) {
        errorMessage.textContent = 'Username and password are required.';
        return;
      }

      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.status === 'success') {
          errorMessage.style.color = 'green';
          errorMessage.textContent = 'Login successful! Redirecting...';
          setTimeout(() => {
            window.location.href = '/catalogue.html';
          }, 1000);
        } else {
          errorMessage.textContent = data.message || 'Login failed.';
        }
      } catch (err) {
        errorMessage.textContent = 'Network error. Please try again later.';
      }
    });
    return; 
  }

  const API_BASE_URL = '/api/catalogues';
  const catalogueList = document.getElementById('catalogueList');
  const refreshBtn = document.getElementById('refreshBtn');
  const createForm = document.getElementById('createForm');
  const editForm = document.getElementById('editForm');
  const cancelEdit = document.getElementById('cancelEdit');
  const editSection = document.getElementById('editSection');
  const createSection = document.getElementById('createSection');
  const createToggleBtn = document.getElementById('createToggleBtn');
  const searchBtn = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchId');
  const clearBtn = document.getElementById('clearBtn');
  const statusFilter = document.getElementById('statusFilter');
  const cancelCreate = document.getElementById('cancelCreate');

  let currentPage = 1;
  const ITEMS_PER_PAGE = 9;
  let allCatalogues = [];

  if (createForm) createForm.addEventListener('submit', handleCreate);
  if (editForm) editForm.addEventListener('submit', handleUpdate);
  if (cancelEdit) cancelEdit.addEventListener('click', () => {
    editForm.reset();
    editSection.style.display = 'none';
  });

  if (cancelCreate) cancelCreate.addEventListener('click', () => {
    createForm.reset();
    createSection.style.display = 'none';
  });

  if (createToggleBtn) createToggleBtn.addEventListener('click', () => {
    createSection.style.display = createSection.style.display === 'none' ? 'block' : 'none';
  });

  if (refreshBtn) refreshBtn.addEventListener('click', loadCatalogues);
  if (clearBtn) clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    statusFilter.value = 'all';
    loadCatalogues();
  });

  if (searchBtn) {
    searchBtn.addEventListener('click', async () => {
      const id = searchInput.value.trim();
      if (!id) {
        alert('Please enter a Catalogue ID.');
        return;
      }
      try {
        const res = await fetch(`${API_BASE_URL}/${id}`);
        const data = await res.json();
        if (data.status === 'success') {
          allCatalogues = [data.data];
          currentPage = 1;
          renderFilteredPage();
        } else {
          catalogueList.innerHTML = `<p>No catalogue found with ID ${id}.</p>`;
          document.getElementById('pagination')?.remove();
        }
      } catch {
        alert('Failed to search catalogue.');
      }
    });
  }

  if (statusFilter) {
    statusFilter.addEventListener('change', () => {
      currentPage = 1;
      renderFilteredPage();
    });
  }

  async function loadCatalogues() {
    try {
      const res = await fetch(API_BASE_URL);
      const data = await res.json();
      if (data.status === 'success') {
        allCatalogues = data.data.reverse(); // Show latest first
        currentPage = 1;
        renderFilteredPage();
      } else {
        showError(data.message);
      }
    } catch {
      showError('Failed to load catalogues.');
    }
  }

  function renderFilteredPage() {
    let filtered = [...allCatalogues];
    const filter = statusFilter.value;

    if (filter === 'active') {
      filtered = filtered.filter(c => c.active);
    } else if (filter === 'inactive') {
      filtered = filtered.filter(c => !c.active);
    }

    const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
    if (currentPage > totalPages) currentPage = totalPages || 1;

    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const paginated = filtered.slice(start, end);

    displayCatalogues(paginated);
    renderPagination(filtered.length);
  }

  function displayCatalogues(catalogues) {
    catalogueList.innerHTML = '';
    if (!catalogues.length) {
      catalogueList.innerHTML = '<p>No catalogues found.</p>';
      return;
    }

    catalogues.forEach(c => {
      const div = document.createElement('div');
      div.className = 'catalogue-item';
      div.innerHTML = `
        <h3>ID: ${c.catalogue_id}</h3>
        <h4><strong><b>Name:</b></strong> ${c.name}</h4>
        <p><strong>Description:</strong> ${c.description}</p>
        <p><strong>Start_date:</strong> ${formatDate(c.start_date)} </p>
        <p><strong>End_date:</strong> ${formatDate(c.end_date)}<p>
        <p style="margin-top: 10px;">
        <span class="status ${c.active ? 'status-active' : 'status-inactive'}">${c.active ? 'Active' : 'Inactive'}</span></p>

        <div class="actions-split" style="margin-top: 10px;">
          <button class="editBtn yellow-btn" data-id="${c.catalogue_id}">Edit</button>
          <button class="deleteBtn red-btn" data-id="${c.catalogue_id}">Delete</button>
        </div>
      `;
      catalogueList.appendChild(div);
    });

    document.querySelectorAll('.editBtn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const id = e.target.getAttribute('data-id');
        const res = await fetch(`${API_BASE_URL}/${id}`);
        const data = await res.json();
        if (data.status === 'success') {
          const c = data.data;
          document.getElementById('editId').value = c.catalogue_id;
          document.getElementById('editName').value = c.name;
          document.getElementById('editDescription').value = c.description;
          document.getElementById('editStartDate').value = new Date(c.start_date).toISOString().split('T')[0];
          document.getElementById('editEndDate').value = new Date(c.end_date).toISOString().split('T')[0];
          document.getElementById('editActive').checked = c.active;
          editSection.style.display = 'block';
          window.scrollTo({ top: editSection.offsetTop, behavior: 'smooth' });
        }
      });
    });

    document.querySelectorAll('.deleteBtn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const id = e.target.getAttribute('data-id');
        if (!confirm('Are you sure you want to delete this catalogue?')) return;
        try {
          const res = await fetch(`${API_BASE_URL}/${id}`, { method: 'DELETE' });
          const data = await res.json();
          if (data.status === 'success') {
            showSuccess('Catalogue deleted successfully.');
            loadCatalogues();
          } else {
            showError(data.message);
          }
        } catch {
          showError('Failed to delete catalogue.');
        }
      });
    });
  }

  function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    let container = document.getElementById('pagination');

    if (!container) {
      container = document.createElement('div');
      container.id = 'pagination';
      container.className = 'pagination';
      catalogueList.after(container);
    } else {
      container.innerHTML = '';
    }

    const prevBtn = document.createElement('button');
    prevBtn.textContent = '« Prev';
    prevBtn.disabled = currentPage === 1;
    prevBtn.className = 'nav-btn';
    prevBtn.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        renderFilteredPage();
      }
    });
    container.appendChild(prevBtn);

    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement('button');
      btn.textContent = i;
      btn.className = (i === currentPage) ? 'active' : '';
      btn.addEventListener('click', () => {
        currentPage = i;
        renderFilteredPage();
      });
      container.appendChild(btn);
    }

    const nextBtn = document.createElement('button');
    nextBtn.textContent = 'Next »';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.className = 'nav-btn';
    nextBtn.addEventListener('click', () => {
      if (currentPage < totalPages) {
        currentPage++;
        renderFilteredPage();
      }
    });
    container.appendChild(nextBtn);
  }

  async function handleCreate(e) {
    e.preventDefault();
    const newCatalogue = {
      name: document.getElementById('name').value,
      description: document.getElementById('description').value,
      start_date: document.getElementById('startDate').value,
      end_date: document.getElementById('endDate').value,
      active: document.getElementById('active').checked
    };
    try {
      const res = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newCatalogue)
      });
      const data = await res.json();
      if (data.status === 'success') {
        showSuccess('Catalogue created successfully.');
        createForm.reset();
        createSection.style.display = 'none';
        loadCatalogues();
      } else {
        showError(data.message);
      }
    } catch {
      showError('Failed to create catalogue.');
    }
  }

  async function handleUpdate(e) {
    e.preventDefault();
    const id = document.getElementById('editId').value;
    const updated = {
      name: document.getElementById('editName').value,
      description: document.getElementById('editDescription').value,
      start_date: document.getElementById('editStartDate').value,
      end_date: document.getElementById('editEndDate').value,
      active: document.getElementById('editActive').checked
    };
    try {
      const res = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updated)
      });
      const data = await res.json();
      if (data.status === 'success') {
        showSuccess('Catalogue updated.');
        editForm.reset();
        editSection.style.display = 'none';
        loadCatalogues();
      } else {
        showError(data.message);
      }
    } catch {
      showError('Failed to update.');
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  function showSuccess(msg) {
    alert(msg);
  }

  function showError(msg) {
    alert(msg);
  }

  loadCatalogues();
});

  
