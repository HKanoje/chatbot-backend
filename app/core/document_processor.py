# app/core/document_processor.py
import os
from typing import List, Dict, Tuple
import PyPDF2
import openpyxl
import pandas as pd
from PIL import Image
import pytesseract
from app.utils.logger import logger
from app.utils.text_utils import clean_text, chunk_text

class DocumentProcessor:
    """Process various document types and extract text"""
    
    def __init__(self):
        """Initialize document processor"""
        self.supported_types = {
            'pdf': self._process_pdf,
            'txt': self._process_txt,
            'xlsx': self._process_excel,
            'xls': self._process_excel,
            'png': self._process_image,
            'jpg': self._process_image,
            'jpeg': self._process_image,
        }
    
    async def process_document(self, file_path: str) -> Tuple[List[str], Dict]:
        """
        Process document and extract text chunks
        
        Args:
            file_path: Path to document file
            
        Returns:
            Tuple of (text_chunks, metadata)
        """
        try:
            # Get file extension
            file_ext = file_path.split('.')[-1].lower()
            filename = os.path.basename(file_path)
            
            if file_ext not in self.supported_types:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            # Extract text using appropriate processor
            logger.info(f"Processing document: {filename}")
            text = await self.supported_types[file_ext](file_path)
            
            # Clean text
            text = clean_text(text)
            
            if not text.strip():
                raise ValueError("No text could be extracted from document")
            
            # Chunk text
            chunks = chunk_text(text, chunk_size=1000, overlap=200)
            
            # Create metadata
            metadata = {
                'filename': filename,
                'file_type': file_ext,
                'total_chunks': len(chunks),
            }
            
            logger.info(f"Extracted {len(chunks)} chunks from {filename}")
            return chunks, metadata
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            raise
    
    async def _process_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise ValueError(f"Failed to process PDF: {str(e)}")
    
    async def _process_txt(self, file_path: str) -> str:
        """
        Extract text from text file
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except UnicodeDecodeError:
            # Try different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                return text
            except Exception as e:
                logger.error(f"Error processing text file: {e}")
                raise ValueError(f"Failed to process text file: {str(e)}")
    
    async def _process_excel(self, file_path: str) -> str:
        """
        Extract text from Excel file
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Extracted text from all sheets
        """
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            text_parts = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Convert dataframe to text
                # Include column names
                text_parts.append(f"Sheet: {sheet_name}\n")
                text_parts.append(df.to_string(index=False))
                text_parts.append("\n\n")
            
            return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error processing Excel file: {e}")
            raise ValueError(f"Failed to process Excel file: {str(e)}")
    
    async def _process_image(self, file_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            file_path: Path to image file
            
        Returns:
            Extracted text via OCR
        """
        try:
            # Open image
            image = Image.open(file_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            if not text.strip():
                raise ValueError("No text could be extracted from image")
            
            return text
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            # Check if tesseract is installed
            if "tesseract" in str(e).lower():
                raise ValueError(
                    "Tesseract OCR is not installed. "
                    "Please install it: https://github.com/tesseract-ocr/tesseract"
                )
            raise ValueError(f"Failed to process image: {str(e)}")

# Create global instance
document_processor = DocumentProcessor()