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
    'csv'
];


// joining path of directory
const mainDirectoryPath = path.join(__dirname, 'files', `training${process.argv[2]}`);

// Asynchronious implementation of forEach loop
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

const mainFunc = async () => {
    // Get all files of directory
    const files = await fs.promises.readdir(mainDirectoryPath);
    // Shuffle for random order of data
    shuffle(files);
    const totalFiles = files.length;
    let count = 0;
    // Read each file and create its byte-histogram and entropy
    await asyncForEach(files, async (file) => {
        fs.readFile(path.join(mainDirectoryPath, file.toString()), function (err, data) {
            if (err) { console.log(err) };
            count += 1;
            console.log(`Starting file ${count} / ${totalFiles}  ${file.toString()}`)
            const fileType = file.toString().split('.')[1];
            const byteData = Uint8Array.from(data);
            const dataLength = byteData.length;
            const histogram = [];
            for (let i = 0; i < 256 * 256; i++)
                histogram[i] = 0;
            for (let i = 0; i < byteData.length - 1; i++) {
                let cb = byteData[i];
                let nb = byteData[i + 1];
                histogram[cb * 256 + nb] += 1;
            }
            const finalHistogram = histogram.map(b => (b / dataLength));
            fs.appendFileSync(`biCsvs/train${process.argv[3]}.csv`, `${finalHistogram.join(',')},${fileType}\n`);
        });
    });
}

mainFunc();