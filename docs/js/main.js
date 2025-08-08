// Initialize AOS
AOS.init({
    duration: 1000,
    once: true,
    offset: 100
});

// Mobile Navigation
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            // Close mobile menu if open
            navMenu.classList.remove('active');
        }
    });
});

// Demo Variables
let isConnected = false;
let analyzing = false;
let organizing = false;

// Demo Functions
function startDemo() {
    document.getElementById('home').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => {
        document.getElementById('demo').scrollIntoView({ behavior: 'smooth' });
    }, 500);
}

function connectDrive() {
    const statusText = document.getElementById('statusText');
    const statusIndicator = document.getElementById('statusIndicator');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const demoContent = document.getElementById('demoContent');
    
    // Simulate OAuth process
    statusText.textContent = 'Google 인증 중...';
    statusIndicator.classList.add('connected');
    
    setTimeout(() => {
        isConnected = true;
        statusText.textContent = '연결됨';
        analyzeBtn.disabled = false;
        
        // Show connected state
        demoContent.innerHTML = `
            <div class="drive-view">
                <h4><i class="fab fa-google-drive"></i> aiden.kim@ggproduction.net</h4>
                <div class="drive-stats">
                    <div class="stat-item">
                        <span class="stat-label">총 파일</span>
                        <span class="stat-value">460</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">총 폴더</span>
                        <span class="stat-value">35</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">사용 공간</span>
                        <span class="stat-value">75.2 GB</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">루트 파일</span>
                        <span class="stat-value" style="color: var(--danger-color);">137</span>
                    </div>
                </div>
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    루트 폴더에 137개의 정리되지 않은 파일이 있습니다.
                </div>
            </div>
        `;
        
        // Show notification
        showNotification('Google Drive 연결 성공!', 'success');
    }, 2000);
}

function analyzeDrive() {
    if (!isConnected || analyzing) return;
    
    analyzing = true;
    const organizeBtn = document.getElementById('organizeBtn');
    const demoContent = document.getElementById('demoContent');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const statusText = document.getElementById('statusText');
    
    statusText.textContent = '드라이브 분석 중...';
    progressBar.style.display = 'block';
    
    // Simulate analysis progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressFill.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            analyzing = false;
            organizeBtn.disabled = false;
            statusText.textContent = '분석 완료';
            
            // Show analysis results
            demoContent.innerHTML = `
                <div class="analysis-results">
                    <h4>📊 분석 결과</h4>
                    <div class="result-grid">
                        <div class="result-card">
                            <h5>파일 타입 분포</h5>
                            <ul>
                                <li>문서: 107개</li>
                                <li>스프레드시트: 92개</li>
                                <li>프레젠테이션: 70개</li>
                                <li>동영상: 92개</li>
                                <li>이미지: 92개</li>
                            </ul>
                        </div>
                        <div class="result-card">
                            <h5>정리 필요 항목</h5>
                            <ul>
                                <li>루트 파일: 137개</li>
                                <li>중복 파일: 23개</li>
                                <li>6개월 이상: 217개</li>
                                <li>임시 파일: 12개</li>
                            </ul>
                        </div>
                        <div class="result-card">
                            <h5>예상 결과</h5>
                            <ul>
                                <li>폴더 생성: 75개</li>
                                <li>파일 이동: 137개</li>
                                <li>공간 절약: 2.3 GB</li>
                                <li>정리 시간: 3-5분</li>
                            </ul>
                        </div>
                    </div>
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        AI가 파일 패턴을 분석했습니다. "자동 정리 시작"을 클릭하여 정리를 시작하세요.
                    </div>
                </div>
            `;
            
            progressBar.style.display = 'none';
            showNotification('분석 완료! 137개 파일을 정리할 수 있습니다.', 'info');
        }
    }, 300);
}

function organizeDrive() {
    if (!isConnected || organizing) return;
    
    organizing = true;
    const demoContent = document.getElementById('demoContent');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const statsRow = document.getElementById('statsRow');
    const statusText = document.getElementById('statusText');
    const processedFiles = document.getElementById('processedFiles');
    const organizedFiles = document.getElementById('organizedFiles');
    const savedSpace = document.getElementById('savedSpace');
    
    statusText.textContent = '파일 정리 중...';
    progressBar.style.display = 'block';
    statsRow.style.display = 'flex';
    progressFill.style.width = '0%';
    
    // Show organizing view
    demoContent.innerHTML = `
        <div class="organizing-view">
            <h4>🚀 자동 정리 진행 중</h4>
            <div class="organizing-log" id="organizingLog">
                <div class="log-entry">폴더 구조 생성 중...</div>
            </div>
        </div>
    `;
    
    const log = document.getElementById('organizingLog');
    let processed = 0;
    let organized = 0;
    let saved = 0;
    
    // Simulate organizing process
    const tasks = [
        { msg: '01_프로젝트 폴더 생성', files: 10, space: 100 },
        { msg: 'WSOP 관련 파일 이동', files: 15, space: 230 },
        { msg: 'GGPoker 파일 정리', files: 20, space: 450 },
        { msg: '02_운영관리 폴더 생성', files: 8, space: 80 },
        { msg: '보고서 파일 이동', files: 12, space: 120 },
        { msg: '03_개발_및_데이터 구성', files: 5, space: 340 },
        { msg: 'Colab 노트북 정리', files: 6, space: 50 },
        { msg: '04_미디어_자료 정리', files: 25, space: 680 },
        { msg: '동영상 파일 분류', files: 20, space: 450 },
        { msg: '루트 폴더 최종 정리', files: 16, space: 0 }
    ];
    
    let taskIndex = 0;
    const taskInterval = setInterval(() => {
        if (taskIndex < tasks.length) {
            const task = tasks[taskIndex];
            
            // Add log entry
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<i class="fas fa-check"></i> ${task.msg}`;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
            
            // Update stats
            processed += task.files;
            organized += Math.floor(task.files * 0.9);
            saved += task.space;
            
            processedFiles.textContent = processed;
            organizedFiles.textContent = organized;
            savedSpace.textContent = (saved / 1000).toFixed(1) + ' GB';
            
            // Update progress
            progressFill.style.width = ((taskIndex + 1) / tasks.length * 100) + '%';
            
            taskIndex++;
        } else {
            clearInterval(taskInterval);
            organizing = false;
            statusText.textContent = '정리 완료!';
            
            // Show completion
            setTimeout(() => {
                demoContent.innerHTML = `
                    <div class="completion-view">
                        <div class="success-icon">
                            <i class="fas fa-check-circle"></i>
                        </div>
                        <h3>정리 완료!</h3>
                        <div class="completion-stats">
                            <div class="stat">
                                <h4>137</h4>
                                <p>파일 정리됨</p>
                            </div>
                            <div class="stat">
                                <h4>0</h4>
                                <p>루트 폴더 파일</p>
                            </div>
                            <div class="stat">
                                <h4>2.3 GB</h4>
                                <p>공간 절약</p>
                            </div>
                        </div>
                        <p>구글 드라이브가 완벽하게 정리되었습니다!</p>
                        <button class="btn btn-primary" onclick="window.open('https://drive.google.com')">
                            <i class="fas fa-external-link-alt"></i> Google Drive에서 확인
                        </button>
                    </div>
                `;
                
                showNotification('🎉 정리 완료! 루트 폴더가 완전히 깨끗해졌습니다.', 'success');
            }, 1000);
        }
    }, 800);
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Download Structure Template
function downloadStructure() {
    const structure = `Google Drive 최적화 폴더 구조
================================

01_프로젝트/
├── WSOP/
│   ├── 2024_WSOPE/
│   ├── 2025_WSOP/
│   └── Creator_Program/
├── GGPoker_Production/
│   ├── LiveStream/
│   ├── Marketing/
│   └── Performance/
└── YouTube_Content/

02_운영관리/
├── 인력관리/
├── 장비관리/
├── 보고서/
└── 문서보관/

03_개발_및_데이터/
├── Colab_Notebooks/
├── 데이터분석/
└── Archive_MAM/

04_미디어_자료/
├── 동영상/
├── 이미지/
└── 오디오/

05_외부협업/
└── 99_임시/
`;

    const blob = new Blob([structure], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'gdrive_folder_structure.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('폴더 구조 템플릿이 다운로드되었습니다.', 'success');
}

// Add custom styles for demo elements
const style = document.createElement('style');
style.textContent = `
    .drive-view, .analysis-results, .organizing-view, .completion-view {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .drive-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: var(--light-color);
        border-radius: 8px;
    }
    
    .stat-label {
        display: block;
        font-size: 0.8rem;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        display: block;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
    }
    
    .alert {
        padding: 1rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .alert-warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .alert-info {
        background: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .result-card {
        background: var(--light-color);
        padding: 1rem;
        border-radius: 8px;
    }
    
    .result-card h5 {
        color: var(--dark-color);
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .result-card ul {
        list-style: none;
        font-size: 0.85rem;
        color: var(--text-color);
    }
    
    .result-card li {
        padding: 0.25rem 0;
    }
    
    .organizing-log {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        height: 300px;
        overflow-y: auto;
        margin-top: 1rem;
    }
    
    .log-entry {
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        color: var(--text-color);
        animation: slideIn 0.3s ease;
    }
    
    .log-entry i {
        color: var(--secondary-color);
        margin-right: 0.5rem;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .completion-view {
        text-align: center;
        padding: 2rem;
    }
    
    .success-icon {
        font-size: 4rem;
        color: var(--secondary-color);
        margin-bottom: 1rem;
        animation: scaleIn 0.5s ease;
    }
    
    @keyframes scaleIn {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }
    
    .completion-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 2rem 0;
    }
    
    .completion-stats .stat {
        text-align: center;
    }
    
    .completion-stats h4 {
        font-size: 2rem;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .notification {
        position: fixed;
        top: 100px;
        right: -400px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: right 0.3s ease;
        z-index: 10000;
        max-width: 350px;
    }
    
    .notification.show {
        right: 20px;
    }
    
    .notification-success {
        border-left: 4px solid var(--secondary-color);
    }
    
    .notification-success i {
        color: var(--secondary-color);
    }
    
    .notification-error {
        border-left: 4px solid var(--danger-color);
    }
    
    .notification-error i {
        color: var(--danger-color);
    }
    
    .notification-info {
        border-left: 4px solid var(--primary-color);
    }
    
    .notification-info i {
        color: var(--primary-color);
    }
`;

document.head.appendChild(style);

// Range slider value display
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function() {
        const span = this.nextElementSibling;
        if (span) {
            span.textContent = this.value + '%';
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
    } else {
        navbar.style.boxShadow = 'var(--shadow)';
    }
});