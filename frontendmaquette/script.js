// Données de produits
const productsData = [
    { code: 'MAT-001', name: 'Ciment Portland 50kg', category: 'Matériaux', stock: 145, threshold: 50, price: 5000 },
    { code: 'MAT-002', name: 'Sable fin (sac 50kg)', category: 'Matériaux', stock: 8, threshold: 30, price: 2500 },
    { code: 'MAT-003', name: 'Gravier (sac 50kg)', category: 'Matériaux', stock: 42, threshold: 25, price: 3000 },
    
];


// Navigation entre modules
function initNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    const modules = document.querySelectorAll('.module');

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const moduleId = item.getAttribute('data-module');
            
            // Mettre à jour le menu actif
            menuItems.forEach(mi => mi.classList.remove('active'));
            item.classList.add('active');
            
            // Afficher le module correspondant
            modules.forEach(module => module.classList.remove('active'));
            document.getElementById(moduleId).classList.add('active');
        });
    });
}


// Gestion des modales
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Fermer la modale en cliquant en dehors
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Rendre les produits dans le tableau
function renderProducts(products = productsData) {
    const tbody = document.getElementById('productsTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    products.forEach(product => {
        const row = document.createElement('tr');
        
        // Déterminer le statut
        let statusBadge = '';
        if (product.stock < product.threshold * 0.5) {
            statusBadge = '<span class="badge badge-warning">Critique</span>';
        } else if (product.stock < product.threshold) {
            statusBadge = '<span class="badge" style="background-color: #ea580c;">Faible</span>';
        } else {
            statusBadge = '<span class="badge badge-success">OK</span>';
        }
        
        row.innerHTML = `
            <td>${product.code}</td>
            <td>${product.name}</td>
            <td>${product.category}</td>
            <td>${product.stock}</td>
            <td>${product.threshold}</td>
            <td>${product.price.toLocaleString()} FCFA</td>
            <td>${statusBadge}</td>
        `;
        
        tbody.appendChild(row);
    });
    
    // Mettre à jour les statistiques
    updateStockStats(products);
}

// Mettre à jour les stats de stock
function updateStockStats(products) {
    const totalProducts = products.length;
    const lowStock = products.filter(p => p.stock < p.threshold).length;
    const okStock = products.filter(p => p.stock >= p.threshold).length;
    
    const totalEl = document.getElementById('totalProducts');
    const lowEl = document.getElementById('lowStockCount');
    const okEl = document.getElementById('okStockCount');
    
    if (totalEl) totalEl.textContent = totalProducts;
    if (lowEl) lowEl.textContent = lowStock;
    if (okEl) okEl.textContent = okStock;
}

// Recherche de produits
function initStockSearch() {
    const searchInput = document.getElementById('stockSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        
        if (searchTerm === '') {
            renderProducts();
            return;
        }
        
        const filtered = productsData.filter(product => 
            product.name.toLowerCase().includes(searchTerm) ||
            product.category.toLowerCase().includes(searchTerm) ||
            product.code.toLowerCase().includes(searchTerm)
        );
        
        renderProducts(filtered);
    });
}

// Recherche de clients
function initCustomerSearch() {
    const searchInput = document.getElementById('customerSearch');
    if (!searchInput) return;
    
    const table = document.getElementById('customersTable');
    if (!table) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// Ajouter un nouveau produit
function handleAddProduct(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const newProduct = {
        code: formData.get('code'),
        name: formData.get('name'),
        category: formData.get('category'),
        stock: parseInt(formData.get('stock')),
        threshold: parseInt(formData.get('threshold')),
        price: parseInt(formData.get('price'))
    };
    
    // Ajouter au tableau de données
    productsData.push(newProduct);
    
    // Réafficher les produits
    renderProducts();
    
    // Réinitialiser le formulaire
    form.reset();
    
    // Fermer la modale
    closeModal('addProductModal');
    
    // Afficher un message (optionnel)
    alert(`Produit "${newProduct.name}" ajouté avec succès !`);
}

// Empêcher la soumission par défaut des formulaires
function initForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Ne pas ajouter d'écouteur si le formulaire a déjà un onsubmit
        if (!form.getAttribute('onsubmit')) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                alert('Fonctionnalité en développement');
                // Fermer la modale parent
                const modal = form.closest('.modal');
                if (modal) {
                    modal.classList.remove('active');
                }
                form.reset();
            });
        }
    });
}

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    renderProducts();
    initStockSearch();
    initCustomerSearch();
    initForms();
    
    console.log('🚀 Système de Gestion Quincaillerie initialisé');
    console.log(`📦 ${productsData.length} produits chargés`);
});

// Fonction pour imprimer (pour les boutons d'impression)
function printDocument() {
    window.print();
}

// Exporter les données (exemple)
function exportData(type) {
    alert(`Export ${type} - Fonctionnalité à venir`);
}

// Fonctions utilitaires
function formatCurrency(amount) {
    return amount.toLocaleString() + ' FCFA';
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR');
}

// Gestion du clavier (ESC pour fermer les modales)
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            activeModal.classList.remove('active');
        }
    }
});
