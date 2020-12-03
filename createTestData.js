// requiring path and fs modules
const path = require('path');
const fs = require('fs');

const fileTypes = [
    'pdf',
    'html',
    'bmp',
    'jpg',
    'rtf',
    'png',
    'doc',
    'txt',
    'xls',
    'gif',
    'xml',
    'ps',
    'csv',
    'gz'
];

// joining path of directory
const mainDirectoryPath = path.join(__dirname, 'files', `testing${process.argv[2]}`);

// Async implementation for forEach loop
async function asyncForEach(array, callback) {
    for (let index = 0; index < array.length; index++) {
        await callback(array[index], index, array);
    }
}

// Fisher-Yates (aka Knuth) Shuffle
function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
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
    console.log({dataLength})
    if (dataLength <= 4096)
        return byteData
    const start = randomIntFromInterval(0, dataLength - 4096);
    const end = start + 4096;
    return byteData.slice(start, end);
}

const mainFunc = async () => {
    const files = await fs.promises.readdir(mainDirectoryPath);
    shuffle(files);
    const totalFiles = files.length;
    let count = 0;
    await asyncForEach(files, async (file) => {
        fs.readFile(path.join(mainDirectoryPath, file.toString()), function (err, data) {
            if (err) { console.log(err) };
            count += 1;
            console.log(`Starting file ${count} / ${totalFiles}  ${file.toString()}`)
            const fileType = file.toString().split('.')[1];
            const byteArray = Uint8Array.from(data);
            let byteData = getFileFragment(byteArray);
            // let byteData = [];
            // while (!(arrayLength * parseFloat(process.argv[4]) < byteData.length &&
            //     byteData.length < arrayLength * parseFloat(process.argv[5]))) {
            //     byteData = getFileFragment(byteArray);
            // }
            const dataLength = byteData.length;
            console.log({ dataLength });
            const histogram = [];
            for (let i = 0; i < 256; i++)
                histogram[i] = 0;
            byteData.forEach(b => { histogram[b] += 1 });
            const finalHistogram = histogram.map(b => (b / dataLength));
            // let entropy = 0;
            // finalHistogram.forEach(value => {
            //     if (value != 0)
            //         entropy += -value * Math.log2(value);
            // });
            // fs.appendFileSync(`test${process.argv[3]}.csv`, `${finalHistogram.join(',')},${entropy},${fileType}\n`);
            fs.appendFileSync(`csvs/test${process.argv[3]}.csv`, `${finalHistogram.join(',')},${fileType}\n`);
        });
    });
}

mainFunc();