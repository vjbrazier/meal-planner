// Variables/page elements
const measurements = document.getElementsByClassName('measurement');
const spoons_header = document.getElementById('spoons-header');
const spoons = document.getElementById('spoons');

let spoons_needed = {
    'cup' : new Set(),
    'tbsp': new Set(),
    'tsp' : new Set
}

// Converts all decimals inside the ingredient list to their fraction equivalents
for (let i = 0; i < measurements.length; i++) {
    let measurement = measurements[i].innerText;
    let units = ['cup', 'tbsp', 'tsp'];

    // Only runs the below code if a decimal is present in the first place
    if (measurement.includes('.')) {
        // Splits it based on the decimal (this is relevant for mixed fractions)
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


        for (const [decimal, fraction] of Object.entries(replacements)) {
            if (measurement_num.includes(decimal)) { 
                // Updates the spoons needed dict based on replacements that are done
                for (let j = 0; j < units.length; j++) {
                    if (measurement_num.includes(units[j])) {
                        spoons_needed[units[j]].add(fraction);
                    }
                }
                
                measurement_num = measurement_num.replace(decimal, fraction);
                measurements[i].innerText = measurement + measurement_num;
            }
        }
    } else {
        for (let j = 0; j < units.length; j++) {
            if (measurement.includes(units[j])) {
                spoons_needed[units[j]].add(1);
            }
        }
    }
}

// Appends to the list with relevant measurements
for (const [unit, measurements] of Object.entries(spoons_needed)) {
    if (measurements.size != 0) {
        spoons_header.classList.add('visible');
        
        for (const measurement of measurements) {
            spoons.innerText += `${measurement} ${unit}\n`;
        }
    }
}