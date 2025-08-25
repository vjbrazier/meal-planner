// Variables/page elements
const measurements = document.getElementsByClassName('measurements');
const spoons = document.getElementById('spoons');

let spoons_needed = {
    'cup' : new Set(),
    'tbsp': new Set(),
    'tsp' : new Set
}

for (let i = 0; i < measurements.length; i++) {
    let measurement = measurements[i].innerText;

    if (measurement.includes('.')) {
        let measurement_num = measurement.substring(measurement.indexOf('.'));
        measurement = measurement.substring(0, measurement.indexOf('.') || '');

        let replacements = {
            '.125': '⅛',
            '.25' : '¼',
            '.33' : '⅓',
            '.5'  : '½',
            '.66' : '⅔',
            '.75' : '¾'
        };

        let units = ['cup', 'tbsp', 'tsp'];

        for (const [decimal, fraction] of Object.entries(replacements)) {
            if (measurement_num.includes(decimal)) { 
                for (let j = 0; j < units.length; j++) {
                    if (measurement_num.includes(units[j])) {
                        spoons_needed[units[j]].add(fraction);
                    }
                }
                
                measurement_num = measurement_num.replace(decimal, fraction);
                measurements[i].innerText = measurement + measurement_num;
            }
        }
    }
}

for (const [unit, measurements] of Object.entries(spoons_needed)) {
    // console.log(unit);
    // console.log(measurements);

    if (measurements.size != 0) {
        spoons.classList.add('visible');
        
        for (const measurement of measurements) {
            spoons.innerText += `${measurement} ${unit}\n`;
        }
    }
}