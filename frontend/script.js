document.addEventListener('DOMContentLoaded', function () {
    const API_BASE_URL = '/api/catalogues';

    const createForm = document.getElementById('createForm');
    const editForm = document.getElementById('editForm');
    const refreshBtn = document.getElementById('refreshBtn');
    const cancelEdit = document.getElementById('cancelEdit');
    const deleteBtn = document.getElementById('deleteBtn');
    const editSection = document.getElementById('editSection');
    const catalogueList = document.getElementById('catalogueList');
    const searchBtn = document.getElementById('searchBtn');
    const searchId = document.getElementById('searchId');
    const searchResult = document.getElementById('searchResult');

    // Load catalogues on page load
    loadCatalogues();

    // Event bindings
    createForm.addEventListener('submit', handleCreate);
    editForm.addEventListener('submit', handleUpdate);
    cancelEdit.addEventListener('click', () => editSection.style.display = 'none');
    refreshBtn.addEventListener('click', loadCatalogues);
    deleteBtn.addEventListener('click', handleDelete);
    searchBtn.addEventListener('click', handleSearchById);

    async function loadCatalogues() {
        try {
            const res = await fetch(API_BASE_URL);
            const data = await res.json();
            if (data.status === 'success') {
                displayCatalogues(data.data);
            } else {
                showError(data.message);
            }
        } catch (err) {
            showError('Failed to load catalogues.');
        }
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
                <h3>${c.name} <span style="font-size: 0.9rem;">(ID: ${c.catalogue_id})</span></h3>
                <p><strong>Description:</strong> ${c.description}</p>
                <p><strong>Start:</strong> ${formatDate(c.start_date)} | <strong>End:</strong> ${formatDate(c.end_date)}</p>
                <span class="status ${c.active ? 'status-active' : 'status-inactive'}">${c.active ? 'Active' : 'Inactive'}</span>
            `;
            div.onclick = () => showModal(c);
            catalogueList.appendChild(div);
        });
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

    async function handleDelete() {
        const id = document.getElementById('editId').value;
        if (!confirm('Delete this catalogue?')) return;

        try {
            const res = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE'
            });
            const data = await res.json();
            if (data.status === 'success') {
                showSuccess('Deleted successfully.');
                editForm.reset();
                editSection.style.display = 'none';
                loadCatalogues();
            } else {
                showError(data.message);
            }
        } catch {
            showError('Failed to delete.');
        }
    }

    async function handleSearchById() {
        const id = searchId.value.trim();
        searchResult.innerHTML = '';
        if (!id) {
            showError('Enter catalogue ID.');
            return;
        }

        try {
            const res = await fetch(`${API_BASE_URL}/${id}`);
            const data = await res.json();
            if (data.status === 'success') {
                const c = data.data;
                searchResult.innerHTML = `
                    <div class="catalogue-item">
                        <h3>${c.name}</h3>
                        <p><strong>Description:</strong> ${c.description}</p>
                        <p><strong>Start:</strong> ${formatDate(c.start_date)} | <strong>End:</strong> ${formatDate(c.end_date)}</p>
                        <span class="status ${c.active ? 'status-active' : 'status-inactive'}">${c.active ? 'Active' : 'Inactive'}</span>
                        <div class="actions">
                            <button class="btn btn-primary" onclick="editCatalogue(${c.catalogue_id})">Edit</button>
                        </div>
                    </div>
                `;
            } else {
                searchResult.innerHTML = `<p>${data.message || 'Not found.'}</p>`;
            }
        } catch {
            searchResult.innerHTML = `<p>Failed to fetch catalogue.</p>`;
        }
    }

    // Edit function for external button
    window.editCatalogue = async function (id) {
        try {
            const res = await fetch(`${API_BASE_URL}/${id}`);
            const data = await res.json();
            if (data.status === 'success') {
                const c = data.data;
                document.getElementById('editId').value = c.catalogue_id;
                document.getElementById('editName').value = c.name;
                document.getElementById('editDescription').value = c.description;
                document.getElementById('editStartDate').value = c.start_date;
                document.getElementById('editEndDate').value = c.end_date;
                document.getElementById('editActive').checked = c.active;
                editSection.style.display = 'block';
                window.scrollTo({ top: editSection.offsetTop, behavior: 'smooth' });
            } else {
                showError(data.message);
            }
        } catch {
            showError('Failed to fetch.');
        }
    };

    function showModal(c) {
        let modal = document.getElementById('catalogueModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'catalogueModal';
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close-btn" id="closeModal">&times;</span>
                    <h3 id="modalTitle"></h3>
                    <p><strong>Description:</strong> <span id="modalDescription"></span></p>
                    <p><strong>Start Date:</strong> <span id="modalStartDate"></span></p>
                    <p><strong>End Date:</strong> <span id="modalEndDate"></span></p>
                    <p><strong>Status:</strong> <span id="modalStatus"></span></p>
                </div>
            `;
            document.body.appendChild(modal);
        }

        document.getElementById('modalTitle').textContent = `${c.name} (ID: ${c.catalogue_id})`;
        document.getElementById('modalDescription').textContent = c.description;
        document.getElementById('modalStartDate').textContent = formatDate(c.start_date);
        document.getElementById('modalEndDate').textContent = formatDate(c.end_date);
        const statusEl = document.getElementById('modalStatus');
        statusEl.textContent = c.active ? 'Active' : 'Inactive';
        statusEl.className = `status ${c.active ? 'status-active' : 'status-inactive'}`;

        modal.style.display = 'block';

        document.getElementById('closeModal').onclick = () => modal.style.display = 'none';
        window.onclick = (e) => {
            if (e.target == modal) modal.style.display = 'none';
        };
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
        alert(`✅ ${msg}`);
    }

    function showError(msg) {
        alert(`❌ ${msg}`);
    }
});
