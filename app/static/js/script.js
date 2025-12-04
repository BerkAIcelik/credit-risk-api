document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loanForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('resultContainer');
    const resetBtn = document.getElementById('resetBtn');

    // Result Elements
    const resultCard = document.querySelector('.result-card');
    const decisionText = document.getElementById('decisionText');
    const probabilityValue = document.getElementById('probabilityValue');
    const applicationId = document.getElementById('applicationId');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable button and show loading state
        setLoading(true);

        try {
            const formData = new FormData(form);
            const payload = {
                annual_income: parseFloat(formData.get('annual_income')),
                debt_to_income_ratio: parseFloat(formData.get('debt_to_income_ratio')),
                credit_score: parseInt(formData.get('credit_score')),
                loan_amount: parseFloat(formData.get('loan_amount')),
                interest_rate: parseFloat(formData.get('interest_rate')),
                grade_subgrade: formData.get('grade_subgrade'),
                employment_status: formData.get('employment_status'),
                education_level: formData.get('education_level'),
                marital_status: formData.get('marital_status'),
                gender: formData.get('gender'),
                loan_purpose: formData.get('loan_purpose')
            };

            console.log('Sending payload:', payload);

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Something went wrong');
            }

            const result = await response.json();
            displayResult(result);

        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        } finally {
            setLoading(false);
        }
    });

    resetBtn.addEventListener('click', () => {
        form.reset();
        resultContainer.classList.add('hidden');
        form.style.display = 'block';
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.textContent = 'Analyzing...';
            submitBtn.disabled = true;
        } else {
            submitBtn.textContent = 'Analyze Risk';
            submitBtn.disabled = false;
        }
    }

    function displayResult(data) {
        // Hide form, show result
        form.style.display = 'none';
        resultContainer.classList.remove('hidden');

        // Update content
        // Assumes decision is "ONAY" or "RED" based on the backend comments in main.py
        // Adjusting logic to handle common English responses or the specific Turkish ones if they persist.
        // The provided schema snippet didn't explicitly show the values for 'decision', but main.py comment said "ONAY" / "RED".
        // Let's handle generically first, then specific styling.
        
        const isApproved = data.decision === 'ONAY' || data.decision === 'Approved' || data.probability > 0.5; 
        // Note: Logic depends on what the model actually returns. 
        // Looking at entities.py, PredictionResults has decision: str. 
        // I'll stick to displaying the text directly but style based on content if possible.
        
        decisionText.textContent = data.decision === 'ONAY' ? 'Loan Approved' : (data.decision === 'RED' ? 'Loan Rejected' : data.decision);
        
        // Formatting probability
        const probPercent = (data.probability * 100).toFixed(2) + '%';
        probabilityValue.textContent = probPercent;
        
        applicationId.textContent = data.application_id || 'N/A';

        // Styling
        resultCard.classList.remove('success', 'failure');
        if (data.decision === 'ONAY' || data.decision === 'Approved') {
            resultCard.classList.add('success');
        } else {
            resultCard.classList.add('failure');
        }
    }
});