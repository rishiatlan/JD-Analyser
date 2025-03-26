from fastapi import UploadFile
import PyPDF2
from docx import Document
import io

class FileProcessor:
    async def process_file(self, file: UploadFile) -> str:
        """
        Process uploaded file and extract text content
        """
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower()

        if file_extension == 'pdf':
            return await self._process_pdf(content)
        elif file_extension == 'docx':
            return await self._process_docx(content)
        elif file_extension == 'txt':
            return content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    async def _process_pdf(self, content: bytes) -> str:
        """
        Process PDF file and extract text
        """
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error processing PDF file: {str(e)}")

    async def _process_docx(self, content: bytes) -> str:
        """
        Process DOCX file and extract text
        """
        try:
            docx_file = io.BytesIO(content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error processing DOCX file: {str(e)}") 