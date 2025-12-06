const API_BASE = '/api';

function getToken() {
    return localStorage.getItem('access_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        clearTokens();
        window.location.href = '/login';
        return;
    }
    
    return response;
}

function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function setLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

async function login(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    setLoading(btn, true);
    
    try {
        const email = form.email.value;
        const password = form.password.value;
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            setTokens(data.access_token, data.refresh_token);
            showToast('Inicio de sesion exitoso');
            setTimeout(() => window.location.href = '/dashboard', 500);
        } else {
            showToast(data.detail || 'Error al iniciar sesion', 'error');
        }
    } catch (error) {
        showToast('Error de conexion', 'error');
    } finally {
        setLoading(btn, false);
    }
}

async function register(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    setLoading(btn, true);
    
    try {
        const email = form.email.value;
        const password = form.password.value;
        const confirmPassword = form.confirmPassword.value;
        
        if (password !== confirmPassword) {
            showToast('Las contrasenas no coinciden', 'error');
            setLoading(btn, false);
            return;
        }
        
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Cuenta creada exitosamente');
            setTimeout(() => window.location.href = '/login', 1000);
        } else {
            showToast(data.detail || 'Error al registrar', 'error');
        }
    } catch (error) {
        showToast('Error de conexion', 'error');
    } finally {
        setLoading(btn, false);
    }
}

function logout() {
    clearTokens();
    window.location.href = '/login';
}

async function loadTemplates() {
    const response = await apiRequest('/templates');
    if (response && response.ok) {
        return await response.json();
    }
    return [];
}

async function loadApiKeys() {
    const response = await apiRequest('/apikeys');
    if (response && response.ok) {
        return await response.json();
    }
    return [];
}

async function createTemplate(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    setLoading(btn, true);
    
    try {
        const name = form.name.value;
        const content = form.content.value;
        
        const response = await apiRequest('/templates', {
            method: 'POST',
            body: JSON.stringify({ name, content })
        });
        
        if (response && response.ok) {
            showToast('Plantilla creada exitosamente');
            setTimeout(() => window.location.href = '/templates', 500);
        } else {
            const data = await response.json();
            showToast(data.detail || 'Error al crear plantilla', 'error');
        }
    } catch (error) {
        showToast('Error de conexion', 'error');
    } finally {
        setLoading(btn, false);
    }
}

async function deleteTemplate(id) {
    if (!confirm('Esta seguro de eliminar esta plantilla?')) return;
    
    const response = await apiRequest(`/templates/${id}`, { method: 'DELETE' });
    if (response && response.ok) {
        showToast('Plantilla eliminada');
        location.reload();
    } else {
        showToast('Error al eliminar plantilla', 'error');
    }
}

async function createApiKey(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    setLoading(btn, true);
    
    try {
        const name = form.name.value;
        const response = await apiRequest('/apikeys/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
        
        if (response && response.ok) {
            const data = await response.json();
            document.getElementById('newKeyDisplay').textContent = data.key;
            document.getElementById('newKeyModal').style.display = 'block';
            new bootstrap.Modal(document.getElementById('newKeyModal')).show();
            form.reset();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Error al crear API Key', 'error');
        }
    } catch (error) {
        showToast('Error de conexion', 'error');
    } finally {
        setLoading(btn, false);
    }
}

async function deleteApiKey(id) {
    if (!confirm('Esta seguro de revocar esta API Key?')) return;
    
    const response = await apiRequest(`/apikeys/${id}`, { method: 'DELETE' });
    if (response && response.ok) {
        showToast('API Key revocada');
        location.reload();
    } else {
        showToast('Error al revocar API Key', 'error');
    }
}

async function renderTemplate(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    setLoading(btn, true);
    
    try {
        const templateId = form.template_id.value;
        let data = {};
        
        try {
            data = JSON.parse(form.data.value || '{}');
        } catch (e) {
            showToast('JSON invalido', 'error');
            setLoading(btn, false);
            return;
        }
        
        const response = await fetch(`/api/render/${templateId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: data })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `rendered-${templateId}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            showToast('PDF generado exitosamente');
        } else {
            const data = await response.json();
            showToast(data.detail || 'Error al generar PDF', 'error');
        }
    } catch (error) {
        showToast('Error de conexion', 'error');
    } finally {
        setLoading(btn, false);
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado al portapapeles');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getToken();
    const publicPages = ['/login', '/register', '/'];
    const currentPath = window.location.pathname;
    
    if (!token && !publicPages.includes(currentPath)) {
        window.location.href = '/login';
    }
});
