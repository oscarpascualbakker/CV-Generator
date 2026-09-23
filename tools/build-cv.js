// Generador de CV en una columna, seguro para ATS.
// Sin tablas, sin cuadros de texto, sin cabeceras ni pies, sin columnas.
//
// Este fichero es SOLO el renderizador: helpers de layout + ensamblado del DOCX.
// No contiene datos de nadie. El contenido del CV (nombre, contacto, experiencia)
// vive en `candidaturas/<carpeta>/cv-content.js`, que NO se versiona. Se indica con CV_CONTENT:
//   CV_CONTENT=candidaturas/<carpeta>/cv-content.js node tools/build-cv.js <salida.docx>
// El contenido real se genera a partir del banco de evidencias (CARRERA-EVIDENCIAS.md).
const {
  Document, Packer, Paragraph, TextRun, BorderStyle,
} = require('docx');
const fs = require('fs');
const path = require('path');

const BLUE = '1F4E79';
const BODY = '2B2B2B';
const GREY = '5A5A5A';
const FONT = 'Arial';

const r = (text, o = {}) => new TextRun({
  text, font: FONT, color: o.color || BODY, size: o.size || 19, bold: !!o.bold,
});

// --- helpers ---
const name = (t) => new Paragraph({ spacing: { after: 60 }, children: [r(t, { size: 40, bold: true, color: BLUE })] });

const headline = (t) => new Paragraph({ spacing: { after: 80 }, children: [r(t, { size: 22, color: BODY })] });

// Línea de contacto en el cuerpo del documento, nunca en la cabecera de página.
const contact = (t) => new Paragraph({ spacing: { after: 60 }, children: [r(t, { size: 18, color: GREY })] });

const section = (t) => new Paragraph({
  spacing: { before: 200, after: 110 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 4 } },
  children: [r(t, { size: 21, bold: true, color: BLUE })],
});

const para = (parts) => new Paragraph({
  spacing: { after: 80, line: 264 },
  children: parts.map(([t, b]) => r(t, { size: 19, bold: !!b })),
});

// "Etiqueta: valor, valor, valor" en texto plano. Es como mejor lo indexan los parsers.
const skillLine = (label, items) => new Paragraph({
  spacing: { after: 70, line: 264 },
  children: [r(label + ': ', { size: 19, bold: true }), r(items, { size: 19 })],
});

// Título del puesto en su propia línea. Empresa, ubicación y fechas en la siguiente,
// separadas por barras. Sin tabuladores ni alineaciones a la derecha.
const jobTitle = (t) => new Paragraph({ spacing: { before: 170, after: 20 }, children: [r(t, { size: 21, bold: true })] });
const jobMeta = (t) => new Paragraph({ spacing: { after: 90 }, children: [r(t, { size: 18, color: GREY })] });

const bullet = (parts) => new Paragraph({
  bullet: { level: 0 },
  spacing: { after: 62, line: 264 },
  children: parts.map(([t, b]) => r(t, { size: 19, bold: !!b })),
});

const eduLine = (title, where) => new Paragraph({
  spacing: { after: 70 },
  children: [r(title, { size: 19, bold: true }), r('  |  ' + where, { size: 19, color: GREY })],
});

// Firma discreta al cierre. No es un pie de página de Word (esos los ignora el ATS),
// es texto normal en el flujo del documento, así que el parser lo lee sin problemas.
const signature = (t) => new Paragraph({
  spacing: { before: 240 },
  children: [new TextRun({ text: t, font: FONT, italics: true, color: GREY, size: 16 })],
});

// ============ CONTENIDO ============
// Los helpers se pasan al fichero de contenido, que devuelve el array de párrafos.
// El contenido real vive en la carpeta de cada candidatura (no versionada). Si no se
// encuentra, se explica cómo indicarlo.
const helpers = {
  name, headline, contact, section, para, skillLine, jobTitle, jobMeta, bullet, eduLine, signature,
};

const contentPath = process.env.CV_CONTENT
  ? path.resolve(process.env.CV_CONTENT)
  : path.join(__dirname, 'cv-content.js');
if (!fs.existsSync(contentPath)) {
  console.error(
    `No existe ${contentPath}.\n` +
    'Indica la fuente del CV con CV_CONTENT:\n' +
    '  CV_CONTENT=candidaturas/<carpeta>/cv-content.js node tools/build-cv.js <salida.docx>\n' +
    'Para probar con el ejemplo:  CV_CONTENT=tools/cv-content.example.js node tools/build-cv.js prueba.docx',
  );
  process.exit(1);
}

// eslint-disable-next-line import/no-dynamic-require, global-require
const content = require(contentPath)(helpers);

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 720, bottom: 680, left: 880, right: 880 } } },
    children: content,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(process.argv[2], b);
  console.log('written:', process.argv[2]);
});
