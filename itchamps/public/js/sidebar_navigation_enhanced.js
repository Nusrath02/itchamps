/* ==================== ITCHAMPS ENHANCED SIDEBAR NAVIGATION JS - FIXED ==================== */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    $(document).ready(function() {
        initSidebarOnLoad();
    });

    // Also initialize on frappe ready
    frappe.ready(function() {
        initSidebarOnLoad();
    });

    // Initialize on page load and route changes
    $(document).on('frappe:ready page-change', function() {
        initSidebarOnLoad();
    });

    function initSidebarOnLoad() {
        // Add a small delay to ensure DOM is fully loaded
        setTimeout(function() {
            if (!$('.custom-workspace-sidebar').length) {
                console.log('Initializing ITChamps Sidebar...');
                initEnhancedWorkspaceSidebar();
            }
        }, 500);
    }

    function initEnhancedWorkspaceSidebar() {
        // Create the sidebar structure
        createEnhancedSidebar();
        attachEnhancedSidebarEvents();
        loadWorkspaceData();
        
        // Hide default workspace display
        hideDefaultWorkspaceGrid();
    }

    function hideDefaultWorkspaceGrid() {
        // Force hide default workspace elements
        $('.workspace-list, .codex-editor, .standard-sidebar-section').hide();
        $('body').addClass('custom-sidebar-active');
    }

    function createEnhancedSidebar() {
        // Remove existing sidebar if any
        $('.custom-workspace-sidebar, .sidebar-toggle-btn').remove();

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
        console.log('Sidebar HTML created');
    }

    function loadWorkspaceData() {
        // Try to get workspaces from Frappe API
        if (typeof frappe !== 'undefined' && frappe.call) {
            frappe.call({
                method: 'frappe.desk.desktop.get_workspace_sidebar_items',
                callback: function(r) {
                    if (r.message && r.message.pages) {
                        console.log('Loaded workspaces from API:', r.message.pages.length);
                        renderWorkspaces(r.message.pages);
                    } else {
                        console.log('API response empty, using defaults');
                        renderDefaultWorkspaces();
                    }
                },
                error: function(err) {
                    console.log('API error, using defaults:', err);
                    renderDefaultWorkspaces();
                }
            });
        } else {
            console.log('Frappe not available, using defaults');
            renderDefaultWorkspaces();
        }
    }

    function renderWorkspaces(workspaces) {
        const $menu = $('#workspace-sidebar-menu');
        $menu.empty();

        const currentRoute = window.location.pathname;

        workspaces.forEach(function(workspace) {
            if (workspace.public !== 0) {
                const menuItem = createWorkspaceMenuItem(workspace, currentRoute);
                $menu.append(menuItem);
            }
        });

        console.log('Rendered', workspaces.length, 'workspaces');
    }

    function createWorkspaceMenuItem(workspace, currentRoute) {
        const isActive = currentRoute.includes(workspace.name.toLowerCase().replace(/ /g, '-'));
        const icon = getWorkspaceIcon(workspace.title || workspace.name);
        
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
            'Payroll': '💵'
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
        if (typeof frappe !== 'undefined' && frappe.call) {
            frappe.call({
                method: 'frappe.desk.desktop.get_desktop_page',
                args: {
                    page: workspaceName
                },
                callback: function(r) {
                    if (r.message) {
                        renderSubmenu($submenu, r.message, workspaceName);
                    } else {
                        $submenu.html('<div class="submenu-empty">No items available</div>');
                    }
                },
                error: function() {
                    $submenu.html('<div class="submenu-error">Could not load menu</div>');
                }
            });
        }
    }

    function renderSubmenu($submenu, pageData, workspaceName) {
        $submenu.empty();
        let itemCount = 0;

        // Get shortcuts
        if (pageData.shortcuts && pageData.shortcuts.items) {
            pageData.shortcuts.items.forEach(function(shortcut) {
                if (shortcut.link_to) {
                    addSubmenuItem($submenu, shortcut.label, shortcut.link_to, shortcut.type);
                    itemCount++;
                }
            });
        }

        // Get links
        if (pageData.links && pageData.links.items) {
            pageData.links.items.forEach(function(link) {
                if (link.link_to) {
                    addSubmenuItem($submenu, link.label, link.link_to, link.type);
                    itemCount++;
                }
            });
        }

        // If no items found, show message
        if (itemCount === 0) {
            $submenu.html('<div class="submenu-empty">No menu items</div>');
        }

        console.log('Loaded', itemCount, 'items for', workspaceName);
    }

    function addSubmenuItem($submenu, label, linkTo, type) {
        let route = '';
        
        // Build proper route
        if (linkTo.includes('List/')) {
            const doctype = linkTo.split('List/')[1];
            route = '/app/' + doctype.toLowerCase().replace(/ /g, '-');
        } else if (linkTo.includes('Form/')) {
            const parts = linkTo.split('Form/')[1].split('/');
            route = '/app/' + parts[0].toLowerCase().replace(/ /g, '-');
        } else if (linkTo.includes('/app/')) {
            route = linkTo;
        } else {
            route = '/app/' + linkTo.toLowerCase().replace(/ /g, '-');
        }

        const icon = getSubmenuIcon(type);

        const $link = $(`
            <a href="${route}" class="sidebar-submenu-link">
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
            'List': '📋'
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
                    { label: 'Asset Movement', route: '/app/asset-movement' }
                ]
            },
            {
                name: 'Buying',
                title: 'Buying',
                submenus: [
                    { label: 'Supplier', route: '/app/supplier' },
                    { label: 'Purchase Order', route: '/app/purchase-order' },
                    { label: 'Request for Quotation', route: '/app/request-for-quotation' }
                ]
            },
            {
                name: 'Manufacturing',
                title: 'Manufacturing',
                submenus: [
                    { label: 'Work Order', route: '/app/work-order' },
                    { label: 'BOM', route: '/app/bom' },
                    { label: 'Production Plan', route: '/app/production-plan' }
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
                    { label: 'Quality Goal', route: '/app/quality-goal' }
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
                    { label: 'Delivery Note', route: '/app/delivery-note' }
                ]
            },
            {
                name: 'Subcontracting',
                title: 'Subcontracting',
                submenus: [
                    { label: 'Subcontracting Order', route: '/app/subcontracting-order' }
                ]
            },
            {
                name: 'ERPNext Settings',
                title: 'ERPNext Settings',
                submenus: [
                    { label: 'Company', route: '/app/company' },
                    { label: 'Fiscal Year', route: '/app/fiscal-year' }
                ]
            },
            {
                name: 'Frappe HR',
                title: 'Frappe HR',
                submenus: [
                    { label: 'Employee', route: '/app/employee' },
                    { label: 'Attendance', route: '/app/attendance' },
                    { label: 'Leave Application', route: '/app/leave-application' }
                ]
            }
        ];

        const $menu = $('#workspace-sidebar-menu');
        $menu.empty();

        const currentRoute = window.location.pathname;

        defaultWorkspaces.forEach(function(workspace) {
            const isActive = currentRoute.includes(workspace.name.toLowerCase().replace(/ /g, '-'));
            const icon = getWorkspaceIcon(workspace.name);
            
            let submenuHtml = '';
            workspace.submenus.forEach(function(submenu) {
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

        console.log('Rendered default workspaces');
    }

    function attachEnhancedSidebarEvents() {
        // Remove previous event handlers
        $(document).off('click', '.sidebar-menu-link');
        $(document).off('click', '.sidebar-submenu-link');
        $(document).off('click', '.sidebar-toggle-btn');

        // Toggle submenu
        $(document).on('click', '.sidebar-menu-link', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
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
            
            if (typeof frappe !== 'undefined' && frappe.set_route) {
                frappe.set_route(route);
            } else {
                window.location.href = route;
            }
            
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

        console.log('Sidebar events attached');
    }

    function markActiveMenu() {
        const currentPath = window.location.pathname;
        
        // Remove all active classes
        $('.sidebar-menu-link').removeClass('active');
        $('.sidebar-submenu-link').removeClass('active');

        // Mark active submenu
        $('.sidebar-submenu-link').each(function() {
            const route = $(this).attr('href');
            if (currentPath.includes(route)) {
                $(this).addClass('active');
                $(this).closest('.sidebar-menu-item').addClass('expanded');
                $(this).closest('.sidebar-menu-item').find('.sidebar-menu-link').addClass('active');
            }
        });
    }

})();
