// Bloom Scroll Effect
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // Feature 1: NPK to Crops
    const feature1Form = document.getElementById('feature1-form');
    if (feature1Form) {
        feature1Form.addEventListener('submit', (e) => {
            e.preventDefault();
            const N = parseFloat(document.getElementById('N').value);
            const P = parseFloat(document.getElementById('P').value);
            const K = parseFloat(document.getElementById('K').value);
            const crops = ['బియ్యం', 'గోధుమ', 'మొక్కజొన్న'];
            const result = crops.map(crop => {
                const adjN = Math.floor(Math.random() * 11) - 5; // Random adjustment -5 to +5
                const adjP = Math.floor(Math.random() * 11) - 5;
                const adjK = Math.floor(Math.random() * 11) - 5;
                return `${crop}: N ని ${adjN}, P ని ${adjP}, K ని ${adjK} సర్దుబాటు చేయండి`;
            }).join('<br>');
            document.getElementById('result').innerHTML = result;
        });
    }

    // Feature 2: Crop to NPK
    const feature2Form = document.getElementById('feature2-form');
    const cropNPK = {
        'బియ్యం': { N: 100, P: 50, K: 50 },
        'గోధుమ': { N: 80, P: 40, K: 40 },
        'మొక్కజొన్న': { N: 120, P: 60, K: 60 }
    };
    if (feature2Form) {
        feature2Form.addEventListener('submit', (e) => {
            e.preventDefault();
            const crop = document.getElementById('crop').value;
            const npk = cropNPK[crop] || { N: 0, P: 0, K: 0 };
            document.getElementById('result').innerHTML = `${crop} కోసం సిఫార్సు చేసిన NPK: N=${npk.N}, P=${npk.P}, K=${npk.K}`;
        });
    }

    // Feature 3: District and Season to Crops
    const feature3Form = document.getElementById('feature3-form');
    const districtSeasonCrops = {
        'ఆదిలాబాద్': {
            'ఖరీఫ్': ['బియ్యం', 'పత్తి'],
            'రబీ': ['గోధుమ', 'చెరుకు']
        },
        'కరీంనగర్': {
            'ఖరీఫ్': ['బియ్యం', 'మొక్కజొన్న'],
            'రబీ': ['గోధుమ', 'మిరప']
        }
    };
    if (feature3Form) {
        feature3Form.addEventListener('submit', (e) => {
            e.preventDefault();
            const district = document.getElementById('district').value;
            const season = document.getElementById('season').value;
            const crops = districtSeasonCrops[district]?.[season] || [];
            document.getElementById('result').innerHTML = crops.length ? 
                `సిఫార్సు చేసిన పంటలు: ${crops.join(', ')}` : 
                'సిఫార్సులు కనుగొనబడలేదు';
        });
    }
});