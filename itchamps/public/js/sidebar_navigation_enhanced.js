/* ==================== ITCHAMPS ENHANCED SIDEBAR NAVIGATION JS ==================== */

frappe.ready(function() {
    setTimeout(function() {
        initEnhancedWorkspaceSidebar();
    }, 1000);
});

function initEnhancedWorkspaceSidebar() {
    // Check if we're on the desk page
    if (!window.location.pathname.includes('/app')) {
        return;
    }

    // Remove existing sidebar if any
    $('.custom-workspace-sidebar').remove();
    $('.sidebar-toggle-btn').remove();

    // Create the sidebar structure
    createEnhancedSidebar();
    attachEnhancedSidebarEvents();
    loadWorkspaceData();
}

function createEnhancedSidebar() {
    const sidebarHtml = `
        <div class="custom-workspace-sidebar">
            <div class="sidebar-header">
                <h3>🏢 Workspaces</h3>
            </div>
            <div class="sidebar-menu" id="workspace-sidebar-menu">
                <div class="sidebar-loading">
                    <div class="loading-spinner"></div>
                    <p>Loading workspaces...</p>
                </div>
            </div>
        </div>
        <button class="sidebar-toggle-btn" title="Toggle Sidebar">
            <span class="toggle-icon">◀</span>
        </button>
    `;

    $('body').append(sidebarHtml);
}

function loadWorkspaceData() {
    // Get all workspaces
    frappe.call({
        method: 'frappe.desk.desktop.get_workspace_sidebar_items',
        callback: function(r) {
            if (r.message) {
                renderWorkspaces(r.message);
            } else {
                // Fallback to default workspaces if API fails
                renderDefaultWorkspaces();
            }
        },
        error: function() {
            renderDefaultWorkspaces();
        }
    });
}

function renderWorkspaces(workspaces) {
    const $menu = $('#workspace-sidebar-menu');
    $menu.empty();

    // Get current page to mark active
    const currentRoute = frappe.get_route_str();

    workspaces.pages.forEach(workspace => {
        if (!workspace.public || workspace.public === 1) {
            const menuItem = createWorkspaceMenuItem(workspace, currentRoute);
            $menu.append(menuItem);
        }
    });
}

function createWorkspaceMenuItem(workspace, currentRoute) {
    const isActive = currentRoute.includes(workspace.name.toLowerCase().replace(/ /g, '-'));
    const icon = getWorkspaceIcon(workspace.name);
    
    const $item = $(`
        <div class="sidebar-menu-item" data-workspace="${workspace.name}">
            <div class="sidebar-menu-link ${isActive ? 'active' : ''}">
                <span class="sidebar-menu-icon">${icon}</span>
                <span class="sidebar-menu-text">${workspace.title || workspace.name}</span>
                <span class="sidebar-menu-arrow">▶</span>
            </div>
            <div class="sidebar-submenu">
                <div class="submenu-loading">Loading...</div>
            </div>
        </div>
    `);

    return $item;
}

function getWorkspaceIcon(workspaceName) {
    const icons = {
        'Framework': '⚙️',
        'Accounts': '💰',
        'Assets': '🏭',
        'Buying': '🛒',
        'Manufacturing': '🏭',
        'Projects': '📊',
        'Quality': '✅',
        'Selling': '💼',
        'Stock': '📦',
        'Subcontracting': '🔄',
        'ERPNext Settings': '⚙️',
        'Frappe HR': '👥',
        'HR': '👥',
        'CRM': '📞',
        'Support': '🎧',
        'Website': '🌐',
        'Payroll': '💵',
        'Loan Management': '💳',
        'Healthcare': '🏥',
        'Education': '🎓',
        'Agriculture': '🌾',
        'Non Profit': '🤝',
        'Hospitality': '🏨'
    };

    return icons[workspaceName] || '📁';
}

function loadWorkspaceSubmenu($menuItem, workspaceName) {
    const $submenu = $menuItem.find('.sidebar-submenu');
    
    // Check if already loaded
    if ($submenu.find('.sidebar-submenu-link').length > 0) {
        return;
    }

    // Load workspace page data
    frappe.call({
        method: 'frappe.desk.desktop.get_desktop_page',
        args: {
            page: workspaceName
        },
        callback: function(r) {
            if (r.message) {
                renderSubmenu($submenu, r.message, workspaceName);
            }
        },
        error: function() {
            $submenu.html('<div class="submenu-error">Could not load menu items</div>');
        }
    });
}

function renderSubmenu($submenu, pageData, workspaceName) {
    $submenu.empty();

    // Get shortcuts from the workspace
    if (pageData.charts && pageData.charts.items) {
        pageData.charts.items.forEach(item => {
            if (item.link_to) {
                addSubmenuItem($submenu, item.label, item.link_to, getSubmenuIcon(item.type));
            }
        });
    }

    // Get shortcuts
    if (pageData.shortcuts && pageData.shortcuts.items) {
        pageData.shortcuts.items.forEach(shortcut => {
            if (shortcut.link_to) {
                addSubmenuItem($submenu, shortcut.label, shortcut.link_to, getSubmenuIcon(shortcut.type));
            }
        });
    }

    // Get links
    if (pageData.links && pageData.links.items) {
        pageData.links.items.forEach(link => {
            if (link.link_to) {
                addSubmenuItem($submenu, link.label, link.link_to, getSubmenuIcon(link.type));
            }
        });
    }

    // If no items found, show message
    if ($submenu.children().length === 0) {
        $submenu.html('<div class="submenu-empty">No menu items available</div>');
    }
}

function addSubmenuItem($submenu, label, linkTo, icon) {
    // Build route based on link type
    let route = '';
    
    if (linkTo.includes('List/')) {
        const doctype = linkTo.split('List/')[1];
        route = `/app/${doctype.toLowerCase().replace(/ /g, '-')}`;
    } else if (linkTo.includes('Form/')) {
        const parts = linkTo.split('Form/')[1].split('/');
        const doctype = parts[0];
        route = `/app/${doctype.toLowerCase().replace(/ /g, '-')}`;
    } else if (linkTo.startsWith('Tree/')) {
        const doctype = linkTo.split('Tree/')[1];
        route = `/app/${doctype.toLowerCase().replace(/ /g, '-')}/view/tree`;
    } else if (linkTo.startsWith('/')) {
        route = linkTo;
    } else {
        route = `/app/${linkTo.toLowerCase().replace(/ /g, '-')}`;
    }

    const $link = $(`
        <a href="${route}" class="sidebar-submenu-link" data-route="${route}">
            <span class="sidebar-submenu-icon">${icon}</span>
            ${label}
        </a>
    `);

    $submenu.append($link);
}

function getSubmenuIcon(type) {
    const icons = {
        'DocType': '📄',
        'Report': '📊',
        'Page': '📃',
        'Dashboard': '📈',
        'List': '📋',
        'Link': '🔗',
        'Help': '❓'
    };
    return icons[type] || '📎';
}

function renderDefaultWorkspaces() {
    const defaultWorkspaces = [
        {
            name: 'Framework',
            title: 'Framework',
            submenus: [
                { label: 'User', route: '/app/user' },
                { label: 'Role', route: '/app/role' },
                { label: 'Module Def', route: '/app/module-def' },
                { label: 'Workspace', route: '/app/workspace' }
            ]
        },
        {
            name: 'Accounts',
            title: 'Accounts',
            submenus: [
                { label: 'Chart of Accounts', route: '/app/chart-of-accounts' },
                { label: 'Journal Entry', route: '/app/journal-entry' },
                { label: 'Sales Invoice', route: '/app/sales-invoice' },
                { label: 'Purchase Invoice', route: '/app/purchase-invoice' },
                { label: 'Payment Entry', route: '/app/payment-entry' }
            ]
        },
        {
            name: 'Assets',
            title: 'Assets',
            submenus: [
                { label: 'Asset', route: '/app/asset' },
                { label: 'Asset Category', route: '/app/asset-category' },
                { label: 'Asset Movement', route: '/app/asset-movement' },
                { label: 'Asset Maintenance', route: '/app/asset-maintenance' }
            ]
        },
        {
            name: 'Buying',
            title: 'Buying',
            submenus: [
                { label: 'Supplier', route: '/app/supplier' },
                { label: 'Purchase Order', route: '/app/purchase-order' },
                { label: 'Request for Quotation', route: '/app/request-for-quotation' },
                { label: 'Supplier Quotation', route: '/app/supplier-quotation' }
            ]
        },
        {
            name: 'Manufacturing',
            title: 'Manufacturing',
            submenus: [
                { label: 'Work Order', route: '/app/work-order' },
                { label: 'BOM', route: '/app/bom' },
                { label: 'Production Plan', route: '/app/production-plan' },
                { label: 'Job Card', route: '/app/job-card' }
            ]
        },
        {
            name: 'Projects',
            title: 'Projects',
            submenus: [
                { label: 'Project', route: '/app/project' },
                { label: 'Task', route: '/app/task' },
                { label: 'Timesheet', route: '/app/timesheet' }
            ]
        },
        {
            name: 'Quality',
            title: 'Quality',
            submenus: [
                { label: 'Quality Inspection', route: '/app/quality-inspection' },
                { label: 'Quality Goal', route: '/app/quality-goal' },
                { label: 'Quality Procedure', route: '/app/quality-procedure' }
            ]
        },
        {
            name: 'Selling',
            title: 'Selling',
            submenus: [
                { label: 'Customer', route: '/app/customer' },
                { label: 'Sales Order', route: '/app/sales-order' },
                { label: 'Quotation', route: '/app/quotation' }
            ]
        },
        {
            name: 'Stock',
            title: 'Stock',
            submenus: [
                { label: 'Item', route: '/app/item' },
                { label: 'Stock Entry', route: '/app/stock-entry' },
                { label: 'Delivery Note', route: '/app/delivery-note' },
                { label: 'Purchase Receipt', route: '/app/purchase-receipt' }
            ]
        },
        {
            name: 'Subcontracting',
            title: 'Subcontracting',
            submenus: [
                { label: 'Subcontracting Order', route: '/app/subcontracting-order' },
                { label: 'Subcontracting Receipt', route: '/app/subcontracting-receipt' }
            ]
        },
        {
            name: 'ERPNext Settings',
            title: 'ERPNext Settings',
            submenus: [
                { label: 'Company', route: '/app/company' },
                { label: 'Fiscal Year', route: '/app/fiscal-year' },
                { label: 'Territory', route: '/app/territory' }
            ]
        },
        {
            name: 'Frappe HR',
            title: 'Frappe HR',
            submenus: [
                { label: 'Employee', route: '/app/employee' },
                { label: 'Attendance', route: '/app/attendance' },
                { label: 'Leave Application', route: '/app/leave-application' },
                { label: 'Salary Structure', route: '/app/salary-structure' },
                { label: 'Payroll Entry', route: '/app/payroll-entry' }
            ]
        }
    ];

    const $menu = $('#workspace-sidebar-menu');
    $menu.empty();

    const currentRoute = frappe.get_route_str();

    defaultWorkspaces.forEach(workspace => {
        const isActive = currentRoute.includes(workspace.name.toLowerCase().replace(/ /g, '-'));
        const icon = getWorkspaceIcon(workspace.name);
        
        let submenuHtml = '';
        workspace.submenus.forEach(submenu => {
            submenuHtml += `
                <a href="${submenu.route}" class="sidebar-submenu-link">
                    <span class="sidebar-submenu-icon">📄</span>
                    ${submenu.label}
                </a>
            `;
        });

        const $item = $(`
            <div class="sidebar-menu-item" data-workspace="${workspace.name}">
                <div class="sidebar-menu-link ${isActive ? 'active' : ''}">
                    <span class="sidebar-menu-icon">${icon}</span>
                    <span class="sidebar-menu-text">${workspace.title}</span>
                    <span class="sidebar-menu-arrow">▶</span>
                </div>
                <div class="sidebar-submenu">
                    ${submenuHtml}
                </div>
            </div>
        `);

        $menu.append($item);
    });
}

function attachEnhancedSidebarEvents() {
    // Toggle submenu
    $(document).on('click', '.sidebar-menu-link', function(e) {
        e.preventDefault();
        const $menuItem = $(this).closest('.sidebar-menu-item');
        const $submenu = $menuItem.find('.sidebar-submenu');
        const workspaceName = $menuItem.data('workspace');

        // If not expanded and submenu not loaded, load it
        if (!$menuItem.hasClass('expanded') && $submenu.find('.submenu-loading').length > 0) {
            loadWorkspaceSubmenu($menuItem, workspaceName);
        }

        // Toggle expansion
        $menuItem.toggleClass('expanded');
        
        // Close other menus
        $('.sidebar-menu-item').not($menuItem).removeClass('expanded');
    });

    // Navigate on submenu click
    $(document).on('click', '.sidebar-submenu-link', function(e) {
        e.preventDefault();
        const route = $(this).attr('href');
        frappe.set_route(route);
        markActiveMenu();
    });

    // Toggle sidebar collapse
    $(document).on('click', '.sidebar-toggle-btn', function() {
        $('body').toggleClass('sidebar-collapsed');
        const $icon = $(this).find('.toggle-icon');
        
        if ($('body').hasClass('sidebar-collapsed')) {
            $icon.text('▶');
        } else {
            $icon.text('◀');
        }
    });

    // Mobile: Open sidebar on toggle
    if ($(window).width() <= 768) {
        $(document).on('click', '.sidebar-toggle-btn', function() {
            $('body').toggleClass('sidebar-open');
        });
    }
}

function markActiveMenu() {
    const currentPath = window.location.pathname;
    const currentRoute = frappe.get_route_str();
    
    // Remove all active classes
    $('.sidebar-menu-link').removeClass('active');
    $('.sidebar-submenu-link').removeClass('active');

    // Mark active submenu
    $('.sidebar-submenu-link').each(function() {
        const route = $(this).attr('href');
        if (currentPath.includes(route) || currentRoute.includes(route)) {
            $(this).addClass('active');
            $(this).closest('.sidebar-menu-item').addClass('expanded');
            $(this).closest('.sidebar-menu-item').find('.sidebar-menu-link').addClass('active');
        }
    });
}

// Re-initialize on route change
$(document).on('page-change', function() {
    markActiveMenu();
});

// Re-initialize on full page load
$(document).on('frappe:ready', function() {
    if (!$('.custom-workspace-sidebar').length) {
        initEnhancedWorkspaceSidebar();
    }
});
