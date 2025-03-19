// Course selection handler
document.getElementById('courseSelect').addEventListener('change', async function() {
    const course = this.value;
    if (!course) return;
    await loadSemesters(course);
});

// Semester selection handler
document.getElementById('semesterSelect').addEventListener('change', async function() {
    const course = document.getElementById('courseSelect').value;
    const semester = this.value;
    if (!semester) return;
    await loadSubjects(course, semester);
});

// Subject selection handler
document.getElementById('subjectSelect').addEventListener('change', async function() {
    const course = document.getElementById('courseSelect').value;
    const semester = document.getElementById('semesterSelect').value;
    const subject = this.value;
    if (!subject) return;
    
    await loadSubjectDetails(course, semester, subject);
    document.getElementById('detailsContainer').classList.remove('hidden');
});

async function loadSemesters(course) {
    try {
        const response = await fetch(`/get_semesters/${course}`);
        const semesters = await response.json();
        
        const semesterSelect = document.getElementById('semesterSelect');
        semesterSelect.innerHTML = '<option value="">Choose Semester</option>';
        
        semesters.forEach(sem => {
            const option = document.createElement('option');
            option.value = sem;
            option.textContent = `Semester ${sem}`;
            semesterSelect.appendChild(option);
        });
        
        document.getElementById('semesterContainer').classList.remove('hidden');
        document.getElementById('subjectContainer').classList.add('hidden');
        document.getElementById('detailsContainer').classList.add('hidden');
    } catch (error) {
        console.error('Error fetching semesters:', error);
    }
}

async function loadSubjects(course, semester) {
    try {
        const response = await fetch(`/get_subjects/${course}/${semester}`);
        const subjects = await response.json();
        
        const subjectSelect = document.getElementById('subjectSelect');
        subjectSelect.innerHTML = '<option value="">Choose Subject</option>';
        
        subjects.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject;
            option.textContent = subject;
            subjectSelect.appendChild(option);
        });
        
        document.getElementById('subjectContainer').classList.remove('hidden');
        document.getElementById('detailsContainer').classList.add('hidden');
    } catch (error) {
        console.error('Error fetching subjects:', error);
    }
}

async function loadSubjectDetails(course, semester, subject) {
    try {
        const response = await fetch(`/get_details/${course}/${semester}/${subject}`);
        const details = await response.json();
        
        const viewSyllabusBtn = document.getElementById('viewSyllabus');
        const getNotesBtn = document.getElementById('getNotes');
        
        viewSyllabusBtn.setAttribute('data-content', details.syllabus);
        getNotesBtn.setAttribute('data-content', details.notes);
        
        viewSyllabusBtn.disabled = !details.syllabus;
        getNotesBtn.disabled = !details.notes;
    } catch (error) {
        console.error('Error fetching subject details:', error);
    }
}

// Button handlers
// Replace the existing viewSyllabus click handler with this one
document.getElementById('viewSyllabus').addEventListener('click', function() {
    const content = this.getAttribute('data-content');
    if (content) {
        const syllabusContainer = document.getElementById('syllabusContainer');
        const syllabusContent = document.getElementById('syllabusContent');
        syllabusContent.innerHTML = content;
        syllabusContainer.classList.remove('hidden');
    }
});

document.getElementById('getNotes').addEventListener('click', function() {
    const notesLink = this.getAttribute('data-content');
    if (notesLink) {
        window.open(notesLink, '_blank');
    }
});

// Contact form handling
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('contactModal');
    const contactBtn = document.getElementById('contactBtn');
    const closeBtn = document.querySelector('.close');
    const contactForm = document.getElementById('contactForm');

    if (!modal || !contactBtn || !closeBtn || !contactForm) {
        console.error('One or more contact form elements not found');
        return;
    }

    contactBtn.addEventListener('click', () => {
        console.log('Contact button clicked');
        modal.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', () => {
        console.log('Close button clicked');
        modal.classList.add('hidden');
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted');

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };
        
        try {
            const response = await fetch('/send_contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('Request sent successfully!');
                modal.classList.add('hidden');
                contactForm.reset();
            } else {
                alert('Failed to send request. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
});


function shareWebsite() {
    if (navigator.share) {
        navigator.share({
            title: 'Fetch2Student',
            text: 'Check out this awesome student resource website!',
            url: window.location.href
        })
        .catch(error => console.log('Error sharing:', error));
    } else {
        // Fallback for browsers that don't support Web Share API
        const dummy = document.createElement('input');
        document.body.appendChild(dummy);
        dummy.value = window.location.href;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        alert('Website URL copied to clipboard!');
    }
}