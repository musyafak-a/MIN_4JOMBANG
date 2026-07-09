// Menunggu elemen sidebar muncul
var checkSidebar = setInterval(function() {
    var nav = document.getElementById('jazzy-navigation');
    if (nav) {
        // Jika belum ada tombol logout, tambahkan
        if (!document.getElementById('custom-logout-btn')) {
            var li = document.createElement('li');
            li.className = 'nav-item mt-4';
            li.id = 'custom-logout-btn';
            li.innerHTML = `
                <a href="/logout/" class="nav-link bg-danger text-white" style="border-radius: 5px;">
                    <i class="nav-icon fas fa-sign-out-alt text-white"></i>
                    <p class="text-white">Logout Guru</p>
                </a>
            `;
            nav.appendChild(li);
        }
        clearInterval(checkSidebar);
    }
}, 200);
