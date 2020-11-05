// requiring path and fs modules
const path = require('path');
const fs = require('fs');

const fileTypes = [
    'pdf',
    'html',
    'jpg',
    'png',
    'doc',
    'txt',
    'xls',
    'ppt',
    'gif',
    'xml',
    'ps',
    'csv',
    'gz',
    'log'
];

// joining path of directory
const mainDirectoryPath = path.join(__dirname, 'files', 'testing');

// Async implementation for forEach loop
async function asyncForEach(array, callback) {
    for (let index = 0; index < array.length; index++) {
        await callback(array[index], index, array);
    }
}

// Get random int between min and max range
function randomIntFromInterval(min, max) {
    let result = Math.floor(Math.random() * (max - min + 1) + min);
    if (result < min) {
        result = min;
    }
    else if (result > max) {
        result = max;
    }
    return result;
}

// Create a fragment of file
const getFileFragment = (byteData) => {
    const dataLength = byteData.length;
    const start = randomIntFromInterval(0, dataLength);
    const end = randomIntFromInterval(start, dataLength);
    return byteData.slice(start, end);
}

const mainFunc = async () => {
    const files = await fs.promises.readdir(mainDirectoryPath);
    const totalFiles = files.length;
    let count = 0;
    await asyncForEach(files, async (file) => {
        fs.readFile(path.join(mainDirectoryPath, file.toString()), function (err, data) {
            if (err) { console.log(err) };
            count += 1;
            console.log(`Starting file ${count} / ${totalFiles}  ${file.toString()}`)
            const fileType = file.toString().split('.')[1];
            let byteData = getFileFragment(Uint8Array.from(data));
            const dataLength = byteData.length;
            const histogram = [];
            for (let i = 0; i < 256; i++)
                histogram[i] = 0;
            byteData.forEach(b => { histogram[b] += 1 });
            const finalHistogram = histogram.map(b => (b / dataLength));
            let entropy = 0;
            finalHistogram.forEach(value => {
                if (value != 0)
                    entropy += -value * Math.log2(value);
            });
            fs.appendFileSync('test.csv', `${finalHistogram.join(',')},${entropy},${fileTypes.indexOf(fileType)}\n`);
        });
    });
}

mainFunc();