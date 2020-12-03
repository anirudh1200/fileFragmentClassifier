const path = require('path');
const fs = require('fs');
const { exec } = require("child_process");

const filePath = process.argv[2];
const absFilePath = path.join(__dirname, filePath);

try {
    fs.unlinkSync('run.csv');
} catch (err) { }

fs.readFile(absFilePath, (err, data) => {
    if (err) console.log(err);
    const byteData = Uint8Array.from(data);
    const dataLength = byteData.length;
    const histogram = [];
    for (let i = 0; i < 256 * 256; i++)
        histogram[i] = 0;
    for (let i = 0; i < dataLength - 1; i++) {
        let cb = byteData[i];
        let nb = byteData[i + 1];
        histogram[cb * 256 + nb] += 1;
    }
    const finalHistogram = histogram.map(b => (b / dataLength));
    fs.appendFileSync('run.csv', finalHistogram.join(','));
    exec("python3 run.py", (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`FileType: ${stdout}`);
    });
});