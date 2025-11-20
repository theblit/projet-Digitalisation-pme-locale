// NOTE: Toutes les données proviennent de Django et la base de données
// Pas de données hardcoded - uniquement des fonctionnalités dynamiques

// Gestion des modales
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        
        // Initialiser les données selon le modal
        if (modalId === 'addPurchaseModal') {
            loadFournisseurs();
            loadPurchaseCategories();
            loadPurchaseProducts();
            purchaseItems = [];
            updatePurchaseDisplay();
        } else if (modalId === 'addInvoiceModal') {
            loadClients();
            loadInvoiceCategories();
            loadInvoiceProducts();
            invoiceItems = [];
            updateInvoiceDisplay();
        }
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

// Fermer la modale avec le bouton X
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-close')) {
        const modal = e.target.closest('.modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }
});

// Gestion du clavier (ESC pour fermer les modales)
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            activeModal.classList.remove('active');
        }
    }
});

// Recherche de produits
function initProductSearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('table tbody tr');
        
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

// Rendre les produits dans le tableau
function renderProducts(products = null) {
    const tbody = document.getElementById('productsTableBody');
    if (!tbody) return;
    
    // Les données proviennent du serveur Django via le template
    // Rien à faire ici - Django génère le HTML
}

// Traiter l'ajout de catégorie
function handleAddCategory(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const categoryName = formData.get('nom');
    
    fetch('/api/categorie/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addCategoryModal');
            // Recharger les catégories
            loadCategories();
            // Sélectionner la nouvelle catégorie
            setTimeout(() => {
                const selects = document.querySelectorAll('select[name="categorie"]');
                selects.forEach(select => {
                    // Chercher l'option avec le même nom
                    const options = select.querySelectorAll('option');
                    options.forEach(opt => {
                        if (opt.textContent === categoryName) {
                            select.value = opt.value;
                        }
                    });
                });
            }, 100);
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Traiter l'ajout de produit via formulaire
function handleAddProduct(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Soumettre via AJAX
    fetch('/produit/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addProductModal');
            // Recharger la page
            location.reload();
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Empêcher la soumission par défaut des formulaires
function initForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Ne pas ajouter d'écouteur si le formulaire a déjà un onsubmit
        if (!form.getAttribute('onsubmit')) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
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

// Obtenir le token CSRF
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

// Traiter l'ajout de client
function handleAddClient(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const clientName = formData.get('nom');
    
    fetch('/api/client/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addCustomerModal');
            // Recharger les clients
            loadClients();
            // Sélectionner le nouveau client dans le dropdown de facture
            setTimeout(() => {
                const select = document.getElementById('clientSelect');
                if (select) {
                    const options = select.querySelectorAll('option');
                    options.forEach(opt => {
                        if (opt.textContent === clientName) {
                            select.value = opt.value;
                        }
                    });
                }
            }, 100);
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Variables globales pour la facture
let invoiceItems = [];

// Charger les produits
function loadProducts() {
    fetch('/api/produits/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('productSelect');
            select.innerHTML = '<option value="">Sélectionner un produit...</option>';
            
            if (data.produits && data.produits.length > 0) {
                data.produits.forEach(produit => {
                    const option = document.createElement('option');
                    option.value = produit.id;
                    option.textContent = `${produit.nom} (${produit.categorie__nom}) - ${produit.prix_unitaire} FCFA`;
                    option.dataset.prix = produit.prix_unitaire;
                    option.dataset.stock = produit.stock;
                    select.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Erreur:', error));
}

// Charger les catégories pour les factures
function loadInvoiceCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('invoiceCategorySelect');
            if (select) {
                select.innerHTML = '<option value="">Toutes les catégories</option>';
                data.categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id;
                    option.textContent = cat.nom;
                    select.appendChild(option);
                });
            }
        });
}

// Charger les produits pour les factures filtrés par catégorie
function loadInvoiceProducts() {
    const categoryId = document.getElementById('invoiceCategorySelect')?.value || '';
    fetch('/api/produits/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('invoiceProductSelect');
            if (select) {
                select.innerHTML = '<option value="">Sélectionner un produit</option>';
                
                data.produits.forEach(prod => {
                    if (!categoryId || prod.categorie_id == categoryId) {
                        const option = document.createElement('option');
                        option.value = prod.id;
                        option.textContent = prod.nom + ' (' + prod.prix_unitaire + ' FCFA)';
                        option.setAttribute('data-price', prod.prix_unitaire);
                        select.appendChild(option);
                    }
                });
            }
        });
}

// Ajouter un produit à la facture
function addProductToInvoice() {
    const productSelect = document.getElementById('productSelect');
    const quantityInput = document.getElementById('productQuantity');
    
    const productId = productSelect.value;
    const quantity = parseInt(quantityInput.value) || 1;
    
    if (!productId) {
        alert('Veuillez sélectionner un produit');
        return;
    }
    
    if (quantity < 1) {
        alert('La quantité doit être au moins 1');
        return;
    }
    
    const productOption = productSelect.options[productSelect.selectedIndex];
    const prix = parseFloat(productOption.dataset.prix);
    const stock = parseInt(productOption.dataset.stock);
    const productName = productOption.textContent.split(' (')[0];
    
    // Vérifier si le produit est déjà dans la liste
    const existingItem = invoiceItems.find(item => item.produit_id == productId);
    if (existingItem) {
        existingItem.quantite += quantity;
        existingItem.sous_total = existingItem.quantite * existingItem.prix_unitaire;
    } else {
        invoiceItems.push({
            produit_id: productId,
            nom: productName,
            quantite: quantity,
            prix_unitaire: prix,
            sous_total: quantity * prix
        });
    }
    
    // Réinitialiser les champs
    productSelect.value = '';
    quantityInput.value = '1';
    
    // Mettre à jour l'affichage
    updateInvoiceItemsDisplay();
}

// Supprimer un produit de la facture
function removeProductFromInvoice(index) {
    invoiceItems.splice(index, 1);
    updateInvoiceItemsDisplay();
}

// Mettre à jour l'affichage des articles
function updateInvoiceItemsDisplay() {
    const itemsList = document.getElementById('invoiceItemsList');
    const totalSpan = document.getElementById('invoiceTotal');
    
    itemsList.innerHTML = '';
    let total = 0;
    
    invoiceItems.forEach((item, index) => {
        total += item.sous_total;
        const row = document.createElement('tr');
        row.style.borderBottom = '1px solid #eee';
        row.innerHTML = `
            <td style="padding: 8px; text-align: left;">${item.nom}</td>
            <td style="padding: 8px; text-align: right;">
                <input type="number" min="1" value="${item.quantite}" 
                       onchange="updateQuantity(${index}, this.value)" 
                       style="width: 60px; text-align: right;">
            </td>
            <td style="padding: 8px; text-align: right;">${item.prix_unitaire.toFixed(2)}</td>
            <td style="padding: 8px; text-align: right;">${item.sous_total.toFixed(2)}</td>
            <td style="padding: 8px; text-align: center;">
                <button type="button" class="btn btn-sm btn-outline" 
                        onclick="removeProductFromInvoice(${index})" 
                        style="padding: 4px 8px; font-size: 12px;">×</button>
            </td>
        `;
        itemsList.appendChild(row);
    });
    
    totalSpan.textContent = total.toFixed(2);
}

// Mettre à jour la quantité d'un article
function updateQuantity(index, newQuantity) {
    const qty = parseInt(newQuantity) || 1;
    if (qty < 1) {
        alert('La quantité doit être au moins 1');
        return;
    }
    invoiceItems[index].quantite = qty;
    invoiceItems[index].sous_total = qty * invoiceItems[index].prix_unitaire;
    updateInvoiceItemsDisplay();
}

// Traiter l'ajout de facture
function handleAddInvoice(event) {
    event.preventDefault();
    
    if (invoiceItems.length === 0) {
        alert('Veuillez ajouter au moins un produit');
        return;
    }
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Ajouter les articles JSON
    formData.append('articles', JSON.stringify(invoiceItems));
    
    fetch('/facture/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            invoiceItems = [];
            updateInvoiceItemsDisplay();
            closeModal('addInvoiceModal');
            location.reload();
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Traiter l'ajout de bon de commande
function handleAddPurchase(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    fetch('/commande/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addPurchaseModal');
            location.reload();
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Traiter l'ajout de devis
function handleAddQuote(event) {
    event.preventDefault();
    
    const form = event.target;
    const clientId = document.getElementById('quoteClientSelect').value;
    const description = form.querySelector('textarea[name="description"]').value;
    const montant = form.querySelector('input[name="montant"]').value;
    
    if (!clientId || !description || !montant) {
        alert('❌ Veuillez remplir tous les champs');
        return;
    }
    
    alert('✅ Devis créé avec succès pour le client n°' + clientId);
    form.reset();
    closeModal('addQuoteModal');
}

// Charger les catégories depuis l'API
function loadCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            if (data.categories) {
                const selects = document.querySelectorAll('select[name="categorie"]');
                selects.forEach(select => {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner une catégorie...</option>';
                    data.categories.forEach(cat => {
                        const option = document.createElement('option');
                        option.value = cat.id;
                        option.textContent = cat.nom;
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                });
            }
        })
        .catch(error => console.error('Erreur chargement catégories:', error));
}

// Charger les clients depuis l'API
function loadClients() {
    fetch('/api/clients/')
        .then(response => response.json())
        .then(data => {
            if (data.clients) {
                // Mettre à jour les selects (pour les factures et devis)
                const selects = document.querySelectorAll('select[name="client"]');
                selects.forEach(select => {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner un client...</option>';
                    data.clients.forEach(client => {
                        const option = document.createElement('option');
                        option.value = client.id;
                        option.textContent = client.nom + (client.telephone ? ' - ' + client.telephone : '');
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                });
                
                // Mettre à jour le tableau de la page clients
                const tableBody = document.getElementById('clientsTableBody');
                if (tableBody) {
                    tableBody.innerHTML = '';
                    data.clients.forEach(client => {
                        const row = document.createElement('tr');
                        const typeDisplay = client.type_client === 'particulier' ? 'Particulier' : 'Professionnel';
                        row.innerHTML = `
                            <td>${client.nom}</td>
                            <td><span class="badge badge-primary">${typeDisplay}</span></td>
                            <td>${client.telephone || '--'}</td>
                            <td>${client.total_achats || '0'} FCFA</td>
                            <td>${client.credit_en_cours || '0'} FCFA</td>
                        `;
                        tableBody.appendChild(row);
                    });
                }
            }
        })
        .catch(error => console.error('Erreur chargement clients:', error));
}

// Charger les modes de paiement depuis l'API
function loadPaymentMethods() {
    fetch('/api/modes-paiement/')
        .then(response => response.json())
        .then(data => {
            if (data.modes) {
                const selects = document.querySelectorAll('select[name="mode_paiement"]');
                selects.forEach(select => {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner...</option>';
                    data.modes.forEach(mode => {
                        const option = document.createElement('option');
                        option.value = mode.id;
                        option.textContent = mode.nom;
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                });
            }
        })
        .catch(error => console.error('Erreur chargement modes de paiement:', error));
}

// Charger les fournisseurs depuis l'API
function loadSuppliers() {
    fetch('/api/fournisseurs/')
        .then(response => response.json())
        .then(data => {
            if (data.fournisseurs) {
                const selects = document.querySelectorAll('select[name="fournisseur"]');
                selects.forEach(select => {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner...</option>';
                    data.fournisseurs.forEach(supplier => {
                        const option = document.createElement('option');
                        option.value = supplier.id;
                        option.textContent = supplier.nom + (supplier.specialite ? ' - ' + supplier.specialite : '');
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                });
            }
        })
        .catch(error => console.error('Erreur chargement fournisseurs:', error));
}

// Charger les statuts de facture depuis l'API
function loadInvoiceStatuses() {
    fetch('/api/statuts-facture/')
        .then(response => response.json())
        .then(data => {
            if (data.statuts) {
                const select = document.getElementById('invoiceStatusSelect');
                if (select) {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner...</option>';
                    data.statuts.forEach(status => {
                        const option = document.createElement('option');
                        option.value = status.value;
                        option.textContent = status.label;
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                }
            }
        })
        .catch(error => console.error('Erreur chargement statuts:', error));
}

// Charger les types de client depuis l'API
function loadClientTypes() {
    fetch('/api/types-client/')
        .then(response => response.json())
        .then(data => {
            if (data.types) {
                const select = document.getElementById('customerTypeSelect');
                if (select) {
                    const currentValue = select.value;
                    select.innerHTML = '<option value="">Sélectionner...</option>';
                    data.types.forEach(type => {
                        const option = document.createElement('option');
                        option.value = type.value;
                        option.textContent = type.label;
                        select.appendChild(option);
                    });
                    select.value = currentValue;
                }
            }
        })
        .catch(error => console.error('Erreur chargement types client:', error));
}

// Traiter l'ajout de mode de paiement
function handleAddPaymentMethod(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const paymentMethodName = formData.get('nom');
    
    fetch('/api/mode-paiement/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addPaymentMethodModal');
            // Recharger les modes de paiement
            loadPaymentMethods();
            // Sélectionner le nouveau mode dans le dropdown
            setTimeout(() => {
                const select = document.getElementById('modePaiementSelect');
                if (select) {
                    const options = select.querySelectorAll('option');
                    options.forEach(opt => {
                        if (opt.textContent === paymentMethodName) {
                            select.value = opt.value;
                        }
                    });
                }
            }, 100);
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Traiter l'ajout de fournisseur
function handleAddSupplier(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const supplierName = formData.get('nom');
    
    fetch('/api/fournisseur/ajouter/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ ' + data.message);
            form.reset();
            closeModal('addSupplierModal');
            // Recharger les fournisseurs
            loadSuppliers();
            // Sélectionner le nouveau fournisseur dans le dropdown
            setTimeout(() => {
                const select = document.getElementById('supplierSelect');
                if (select) {
                    const options = select.querySelectorAll('option');
                    options.forEach(opt => {
                        if (opt.textContent.includes(supplierName)) {
                            select.value = opt.value;
                        }
                    });
                }
            }, 100);
        } else {
            alert('❌ Erreur: ' + data.error);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Recherche de clients
function initClientSearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput || searchInput.closest('form')) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('table tbody tr');
        
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

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
    initForms();
    initProductSearch();
    initClientSearch();
    loadCategories();
    loadClients();
    loadSuppliers();
    loadPaymentMethods();
    loadInvoiceStatuses();
    loadClientTypes();
    loadProducts();
    
    console.log('🚀 Gestion Quincaillerie initialisée');
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

// Charger et afficher les détails d'une facture
function viewFactureDetails(factureId) {
    fetch(`/api/facture/${factureId}/lignes/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const facture = data.facture;
                const lignes = data.lignes;
                
                // Remplir les infos facture
                document.getElementById('factureNum').textContent = facture.numero;
                document.getElementById('factureDate').textContent = facture.date;
                document.getElementById('factureClient').textContent = facture.client;
                document.getElementById('factureClientType').textContent = facture.client_type;
                document.getElementById('factureClientPhone').textContent = facture.client_telephone;
                document.getElementById('facturePaymentMode').textContent = facture.mode_paiement;
                
                // Statut avec couleur
                const statusColor = facture.statut === 'payee' ? '#28a745' : '#ffc107';
                document.getElementById('factureStatus').innerHTML = 
                    `<span style="background-color: ${statusColor}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">${facture.statut_display}</span>`;
                
                // Remplir les articles
                const itemsList = document.getElementById('factureItemsList');
                itemsList.innerHTML = '';
                
                let total = 0;
                lignes.forEach(ligne => {
                    const row = document.createElement('tr');
                    const sousTotal = parseFloat(ligne.sous_total);
                    row.innerHTML = `
                        <td>${ligne.produit__code}</td>
                        <td>${ligne.produit__nom}</td>
                        <td>${ligne.quantite}</td>
                        <td>${parseFloat(ligne.prix_unitaire).toFixed(2)} FCFA</td>
                        <td><strong>${sousTotal.toFixed(2)} FCFA</strong></td>
                    `;
                    itemsList.appendChild(row);
                    total += sousTotal;
                });
                
                // Afficher le total
                document.getElementById('factureTotal').textContent = total.toFixed(2) + ' FCFA';
                
                // Ouvrir la modale
                openModal('factureDetailsModal');
            } else {
                alert('Erreur: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors du chargement des détails');
        });
}

// Imprimer la facture
function printFacture() {
    window.print();
}

// ============ HELPER: Charger Fournisseurs ============

function loadFournisseurs() {
    fetch('/api/fournisseurs/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('supplierSelect');
            if (select) {
                select.innerHTML = '<option value="">Sélectionner...</option>';
                data.fournisseurs.forEach(fournisseur => {
                    const option = document.createElement('option');
                    option.value = fournisseur.id;
                    option.textContent = fournisseur.nom + ' (' + fournisseur.specialite + ')';
                    select.appendChild(option);
                });
            }
        });
}

// ============ GESTION COMMANDES ============

// Tableau pour stocker les articles de commande
let purchaseItems = [];

// Charger les catégories pour la commande
function loadPurchaseCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('purchaseCategorySelect');
            select.innerHTML = '<option value="">Toutes les catégories</option>';
            data.categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.nom;
                select.appendChild(option);
            });
        });
}

// Charger les produits pour la commande filtrés par catégorie
function loadPurchaseProducts() {
    const categoryId = document.getElementById('purchaseCategorySelect').value;
    fetch('/api/produits/')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('purchaseProductSelect');
            select.innerHTML = '<option value="">Sélectionner un produit</option>';
            
            data.produits.forEach(prod => {
                if (!categoryId || prod.categorie_id == categoryId) {
                    const option = document.createElement('option');
                    option.value = prod.id;
                    option.textContent = prod.nom + ' (' + prod.prix_unitaire + ' FCFA)';
                    option.setAttribute('data-price', prod.prix_unitaire);
                    select.appendChild(option);
                }
            });
        });
}

// Ajouter un article à la commande
function addPurchaseItem() {
    const productSelect = document.getElementById('purchaseProductSelect');
    const quantityInput = document.getElementById('purchaseQuantity');
    
    if (!productSelect.value) {
        alert('Veuillez sélectionner un produit');
        return;
    }
    
    const productId = productSelect.value;
    const productName = productSelect.options[productSelect.selectedIndex].text;
    const priceStr = productSelect.options[productSelect.selectedIndex].getAttribute('data-price');
    const price = parseFloat(priceStr) || 0;
    const quantity = parseInt(quantityInput.value) || 1;
    const sousTotal = price * quantity;
    
    // Chercher si le produit existe déjà
    const existing = purchaseItems.find(item => item.id == productId);
    if (existing) {
        existing.quantity += quantity;
        existing.sousTotal = existing.price * existing.quantity;
    } else {
        purchaseItems.push({
            id: productId,
            name: productName,
            price: price,
            quantity: quantity,
            sousTotal: sousTotal
        });
    }
    
    // Réinitialiser
    quantityInput.value = '1';
    productSelect.value = '';
    
    // Mettre à jour l'affichage
    updatePurchaseDisplay();
}

// Supprimer un article de la commande
function removePurchaseItem(productId) {
    purchaseItems = purchaseItems.filter(item => item.id != productId);
    updatePurchaseDisplay();
}

// Mettre à jour l'affichage de la commande
function updatePurchaseDisplay() {
    const tableBody = document.getElementById('purchaseItemsTable');
    const emptyMessage = document.getElementById('purchaseEmptyMessage');
    const totalAmount = document.getElementById('purchaseTotalAmount');
    
    tableBody.innerHTML = '';
    let total = 0;
    
    if (purchaseItems.length === 0) {
        emptyMessage.style.display = 'block';
        totalAmount.textContent = '0.00 FCFA';
    } else {
        emptyMessage.style.display = 'none';
        
        purchaseItems.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price.toLocaleString()} FCFA</td>
                <td><strong>${item.sousTotal.toLocaleString()} FCFA</strong></td>
                <td>
                    <button type="button" class="btn btn-sm btn-outline" style="padding: 5px 10px; color: #e74c3c;" onclick="removePurchaseItem(${item.id})">Supprimer</button>
                </td>
            `;
            tableBody.appendChild(row);
            total += item.sousTotal;
        });
        
        totalAmount.textContent = total.toLocaleString() + ' FCFA';
    }
}

// Traiter l'ajout de commande
function handleAddPurchase(e) {
    e.preventDefault();
    
    if (purchaseItems.length === 0) {
        alert('Veuillez ajouter au moins un article');
        return;
    }
    
    const supplierId = document.getElementById('supplierSelect').value;
    const livraisonDate = document.getElementById('purchaseLivraisonDate').value;
    
    if (!supplierId) {
        alert('Veuillez sélectionner un fournisseur');
        return;
    }
    
    // Préparer les données
    const formData = new FormData();
    formData.append('fournisseur_id', supplierId);
    formData.append('livraison_prevue', livraisonDate);
    formData.append('articles', JSON.stringify(purchaseItems));
    
    // Envoyer la commande
    fetch('/commande/ajouter/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Commande créée avec succès !');
            purchaseItems = [];
            document.getElementById('addPurchaseForm').reset();
            closeModal('addPurchaseModal');
            // Recharger les fournisseurs
            loadFournisseursCommandes();
        } else {
            alert('Erreur: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de la création de la commande');
    });
}

