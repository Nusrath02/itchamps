/* ==================== ITCHAMPS SIDEBAR - COMPLETE FIX ==================== */

(function() {
    'use strict';
    
    console.log('ITChamps Sidebar Module Loading...');
    
    // Initialize when everything is ready
    function initWhenReady() {
        if (typeof frappe === 'undefined' || typeof $ === 'undefined') {
            console.log('Waiting for frappe and jQuery...');
            setTimeout(initWhenReady, 500);
            return;
        }
        
        console.log('Starting sidebar initialization...');
        createSidebar();
        hideDefaultWorkspace();
        attachEvents();
    }
    
    // Start initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWhenReady);
    } else {
        initWhenReady();
    }
    
    // Also re-init on page changes
    $(document).on('page-change', function() {
        if (!$('.custom-workspace-sidebar').length) {
            initWhenReady();
        }
        hideDefaultWorkspace();
    });
    
    function hideDefaultWorkspace() {
        // Aggressively hide all default workspace elements
        setTimeout(function() {
            $('.workspace-list, .codex-editor, .standard-sidebar-section').hide();
            $('.workspace .page-content .workspace-list').hide();
            $('.desk-page .workspace-list').hide();
            console.log('Hidden default workspace elements');
        }, 100);
    }
    
    function createSidebar() {
        // Remove existing
        $('.custom-workspace-sidebar, .sidebar-toggle-btn').remove();
        
        const workspaces = getWorkspaceList();
        
        let menuHtml = '';
        workspaces.forEach(function(ws) {
            menuHtml += `
                <div class="sidebar-menu-item" data-workspace="${ws.name}">
                    <div class="sidebar-menu-link">
                        <span class="sidebar-menu-icon">${ws.icon}</span>
                        <span class="sidebar-menu-text">${ws.title}</span>
                        <span class="sidebar-menu-arrow">▶</span>
                    </div>
                    <div class="sidebar-submenu">
                        ${renderSubmenuItems(ws.items)}
                    </div>
                </div>
            `;
        });
        
        const sidebarHtml = `
            <div class="custom-workspace-sidebar">
                <div class="sidebar-header">
                    <h3>🏢 Workspaces</h3>
                </div>
                <div class="sidebar-menu">
                    ${menuHtml}
                </div>
            </div>
            <button class="sidebar-toggle-btn" title="Toggle Sidebar">
                <span class="toggle-icon">◀</span>
            </button>
        `;
        
        $('body').append(sidebarHtml);
        console.log('Sidebar created with', workspaces.length, 'workspaces');
    }
    
    function renderSubmenuItems(items) {
        if (!items || items.length === 0) {
            return '<div class="submenu-empty">No items</div>';
        }
        
        let html = '';
        items.forEach(function(item) {
            html += `
                <a href="${item.route}" class="sidebar-submenu-link" data-route="${item.route}">
                    <span class="sidebar-submenu-icon">${item.icon}</span>
                    ${item.label}
                </a>
            `;
        });
        
        return html;
    }
    
    function getWorkspaceList() {
        return [
            {
                name: 'Framework',
                title: 'Framework',
                icon: '⚙️',
                items: [
                    { label: 'Automation', route: '/app/automation', icon: '🤖' },
                    { label: 'Build', route: '/app/build', icon: '🏗️' },
                    { label: 'Data', route: '/app/data', icon: '💾' },
                    { label: 'Email', route: '/app/email', icon: '✉️' },
                    { label: 'Integrations', route: '/app/integrations', icon: '🔌' },
                    { label: 'Printing', route: '/app/printing', icon: '🖨️' },
                    { label: 'System', route: '/app/system', icon: '⚙️' },
                    { label: 'Users', route: '/app/user', icon: '👤' },
                    { label: 'Website', route: '/app/website', icon: '🌐' },
                    { label: 'Role', route: '/app/role', icon: '🔑' },
                    { label: 'Module Def', route: '/app/module-def', icon: '📦' },
                    { label: 'Workspace', route: '/app/workspace', icon: '🏢' }
                ]
            },
            {
                name: 'Accounts',
                title: 'Accounts',
                icon: '💰',
                items: [
                    { label: 'Financial Reports', route: '/app/financial-reports', icon: '📊' },
                    { label: 'Accounting', route: '/app/accounting', icon: '💰' },
                    { label: 'Taxes', route: '/app/taxes', icon: '💵' },
                    { label: 'Budget', route: '/app/budget', icon: '💼' },
                    { label: 'Banking', route: '/app/banking', icon: '🏦' },
                    { label: 'Share Management', route: '/app/share-management', icon: '📈' },
                    { label: 'Subscription', route: '/app/subscription', icon: '🔄' },
                    { label: 'Chart of Accounts', route: '/app/chart-of-accounts', icon: '📊' },
                    { label: 'Journal Entry', route: '/app/journal-entry', icon: '📝' },
                    { label: 'Sales Invoice', route: '/app/sales-invoice', icon: '🧾' },
                    { label: 'Purchase Invoice', route: '/app/purchase-invoice', icon: '📄' },
                    { label: 'Payment Entry', route: '/app/payment-entry', icon: '💳' }
                ]
            },
            {
                name: 'Assets',
                title: 'Assets',
                icon: '🏭',
                items: [
                    { label: 'Asset', route: '/app/asset', icon: '🏗️' },
                    { label: 'Location', route: '/app/location', icon: '📍' },
                    { label: 'Asset Category', route: '/app/asset-category', icon: '📁' },
                    { label: 'Asset Movement', route: '/app/asset-movement', icon: '🚚' },
                    { label: 'Asset Maintenance', route: '/app/asset-maintenance', icon: '🔧' },
                    { label: 'Asset Repair', route: '/app/asset-repair', icon: '🛠️' },
                    { label: 'Asset Capitalization', route: '/app/asset-capitalization', icon: '💰' }
                ]
            },
            {
                name: 'Buying',
                title: 'Buying',
                icon: '🛒',
                items: [
                    { label: 'Supplier', route: '/app/supplier', icon: '🏪' },
                    { label: 'Purchase Order', route: '/app/purchase-order', icon: '📋' },
                    { label: 'Material Request', route: '/app/material-request', icon: '📝' },
                    { label: 'Request for Quotation', route: '/app/request-for-quotation', icon: '❓' },
                    { label: 'Supplier Quotation', route: '/app/supplier-quotation', icon: '💬' },
                    { label: 'Purchase Invoice', route: '/app/purchase-invoice', icon: '📄' }
                ]
            },
            {
                name: 'Manufacturing',
                title: 'Manufacturing',
                icon: '🏭',
                items: [
                    { label: 'Work Order', route: '/app/work-order', icon: '⚙️' },
                    { label: 'BOM', route: '/app/bom', icon: '📃' },
                    { label: 'Production Plan', route: '/app/production-plan', icon: '📅' },
                    { label: 'Job Card', route: '/app/job-card', icon: '🎫' },
                    { label: 'Stock Entry', route: '/app/stock-entry', icon: '📦' }
                ]
            },
            {
                name: 'Projects',
                title: 'Projects',
                icon: '📊',
                items: [
                    { label: 'Project', route: '/app/project', icon: '📁' },
                    { label: 'Task', route: '/app/task', icon: '✅' },
                    { label: 'Timesheet', route: '/app/timesheet', icon: '⏱️' },
                    { label: 'Project Template', route: '/app/project-template', icon: '📋' }
                ]
            },
            {
                name: 'Quality',
                title: 'Quality',
                icon: '✅',
                items: [
                    { label: 'Quality Inspection', route: '/app/quality-inspection', icon: '🔍' },
                    { label: 'Quality Goal', route: '/app/quality-goal', icon: '🎯' },
                    { label: 'Quality Review', route: '/app/quality-review', icon: '⭐' },
                    { label: 'Quality Action', route: '/app/quality-action', icon: '✔️' },
                    { label: 'Non Conformance', route: '/app/non-conformance', icon: '⚠️' },
                    { label: 'Quality Feedback', route: '/app/quality-feedback', icon: '💬' },
                    { label: 'Quality Meeting', route: '/app/quality-meeting', icon: '👥' },
                    { label: 'Quality Procedure', route: '/app/quality-procedure', icon: '📝' }
                ]
            },
            {
                name: 'Selling',
                title: 'Selling',
                icon: '💼',
                items: [
                    { label: 'Customer', route: '/app/customer', icon: '👥' },
                    { label: 'Sales Order', route: '/app/sales-order', icon: '📄' },
                    { label: 'Quotation', route: '/app/quotation', icon: '💬' },
                    { label: 'Sales Partner', route: '/app/sales-partner', icon: '🤝' },
                    { label: 'Sales Invoice', route: '/app/sales-invoice', icon: '🧾' }
                ]
            },
            {
                name: 'Stock',
                title: 'Stock',
                icon: '📦',
                items: [
                    { label: 'Item', route: '/app/item', icon: '🏷️' },
                    { label: 'Stock Entry', route: '/app/stock-entry', icon: '📝' },
                    { label: 'Delivery Note', route: '/app/delivery-note', icon: '🚚' },
                    { label: 'Purchase Receipt', route: '/app/purchase-receipt', icon: '📥' },
                    { label: 'Material Request', route: '/app/material-request', icon: '📋' },
                    { label: 'Pick List', route: '/app/pick-list', icon: '📃' }
                ]
            },
            {
                name: 'Subcontracting',
                title: 'Subcontracting',
                icon: '🔄',
                items: [
                    { label: 'Subcontracting BOM', route: '/app/subcontracting-bom', icon: '📋' },
                    { label: 'Subcontracting Order', route: '/app/subcontracting-order', icon: '📄' },
                    { label: 'Subcontracting Receipt', route: '/app/subcontracting-receipt', icon: '📦' }
                ]
            },
            {
                name: 'ERPNext Settings',
                title: 'ERPNext Settings',
                icon: '⚙️',
                items: [
                    { label: 'Global Defaults', route: '/app/global-defaults', icon: '🌐' },
                    { label: 'System Settings', route: '/app/system-settings', icon: '⚙️' },
                    { label: 'Accounts Settings', route: '/app/accounts-settings', icon: '💰' },
                    { label: 'POS Settings', route: '/app/pos-settings', icon: '🏪' },
                    { label: 'Selling Settings', route: '/app/selling-settings', icon: '💼' },
                    { label: 'Buying Settings', route: '/app/buying-settings', icon: '🛒' },
                    { label: 'Stock Settings', route: '/app/stock-settings', icon: '📦' },
                    { label: 'Manufacturing Settings', route: '/app/manufacturing-settings', icon: '🏭' },
                    { label: 'Company', route: '/app/company', icon: '🏢' },
                    { label: 'Fiscal Year', route: '/app/fiscal-year', icon: '📅' },
                    { label: 'Territory', route: '/app/territory', icon: '🗺️' },
                    { label: 'Brand', route: '/app/brand', icon: '🏷️' }
                ]
            },
            {
                name: 'Frappe HR',
                title: 'Frappe HR',
                icon: '👥',
                items: [
                    { label: 'Home', route: '/app/home', icon: '🏠' },
                    { label: 'Build', route: '/app/build', icon: '🏗️' },
                    { label: 'People', route: '/app/people', icon: '👥' },
                    { label: 'Tenure', route: '/app/tenure', icon: '📅' },
                    { label: 'Accounting', route: '/app/accounting', icon: '💰' },
                    { label: 'Recruitment', route: '/app/recruitment', icon: '👔' },
                    { label: 'Shift & Attendance', route: '/app/shift-attendance', icon: '📋' },
                    { label: 'Employee', route: '/app/employee', icon: '👤' },
                    { label: 'Attendance', route: '/app/attendance', icon: '📅' },
                    { label: 'Leave Application', route: '/app/leave-application', icon: '🏖️' },
                    { label: 'Salary Structure', route: '/app/salary-structure', icon: '💰' },
                    { label: 'Payroll Entry', route: '/app/payroll-entry', icon: '💵' }
                ]
            }
        ];
    }
    
    function attachEvents() {
        // Remove old events
        $(document).off('click.sidebar');
        
        // Toggle submenu - PREVENT NAVIGATION
        $(document).on('click.sidebar', '.sidebar-menu-link', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const $menuItem = $(this).closest('.sidebar-menu-item');
            const wasExpanded = $menuItem.hasClass('expanded');
            
            // Close all other menus
            $('.sidebar-menu-item').removeClass('expanded');
            
            // Toggle this menu
            if (!wasExpanded) {
                $menuItem.addClass('expanded');
                console.log('Expanded:', $menuItem.data('workspace'));
            }
        });
        
        // Navigate on submenu link click
        $(document).on('click.sidebar', '.sidebar-submenu-link', function(e) {
            e.preventDefault();
            const route = $(this).data('route');
            console.log('Navigating to:', route);
            frappe.set_route(route);
        });
        
        // Toggle sidebar collapse
        $(document).on('click.sidebar', '.sidebar-toggle-btn', function() {
            $('body').toggleClass('sidebar-collapsed');
            const $icon = $(this).find('.toggle-icon');
            $icon.text($('body').hasClass('sidebar-collapsed') ? '▶' : '◀');
        });
        
        console.log('Sidebar events attached');
    }
    
})();
