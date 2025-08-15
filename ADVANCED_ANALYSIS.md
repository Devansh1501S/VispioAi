# Advanced Image Analysis Features

Vispio now includes powerful advanced analysis capabilities that can identify locations, products, and extract detailed information from images.

## 🔍 Analysis Types

### 1. 📍 Location Analysis
**Purpose**: Identify and analyze locations, places, and geographic context

**What it analyzes**:
- Indoor/outdoor settings and venue types
- Geographic clues from architecture and signage
- Specific identifiers like street names, building names, landmarks
- Environmental context (weather, lighting, time of day)
- Background elements that provide location context
- Readable signs, addresses, and location markers

**Best for**:
- Travel photos
- Real estate images
- Street photography
- Landmark identification
- Geographic research

**Example questions**:
- "Where was this photo taken?"
- "Can you identify this landmark?"
- "What city or country is this?"
- "What type of building is this?"

### 2. 🛍️ Product Analysis
**Purpose**: Identify and analyze products, brands, and commercial items

**What it analyzes**:
- Specific product identification and categorization
- Brand recognition and logo identification
- Product details (model numbers, specifications, materials)
- Text analysis on labels, tags, and packaging
- Price information and market positioning
- Quality assessment and authenticity indicators
- Comparative analysis with similar products
- Usage context and target market

**Best for**:
- E-commerce product photos
- Shopping and retail images
- Brand identification
- Product research
- Market analysis

**Example questions**:
- "What product is this?"
- "Can you identify the brand?"
- "What are the specifications?"
- "How much might this cost?"

### 3. 🔬 Comprehensive Analysis
**Purpose**: Complete detailed analysis combining all aspects

**What it analyzes**:
- Location and setting analysis
- Product and object identification
- Contextual analysis (purpose, story, cultural indicators)
- Technical details (photography style, lighting, composition)
- Specific identifications of people, places, things
- All readable text and identifiable information

**Best for**:
- Complex images with multiple elements
- Research and documentation
- Detailed image cataloging
- Forensic-style analysis

### 4. 📝 Text Extraction
**Purpose**: Extract and analyze all visible text and readable details

**What it extracts**:
- All readable text (signs, labels, documents, screens)
- Numbers and codes (phone numbers, addresses, product codes)
- Identifiable information (brands, companies, websites)
- Location indicators (street names, city names)
- Product information (names, descriptions, instructions)

**Best for**:
- Document analysis
- Sign reading
- Information extraction
- Data collection

### 5. 💬 Smart Chatbot Analysis
**Purpose**: Automatically routes questions to specialized analysis

**How it works**:
- Detects location-related keywords and uses location analysis
- Detects product-related keywords and uses product analysis
- Falls back to general conversation for other questions

**Location keywords**: where, location, place, address, city, country, landmark, building, street
**Product keywords**: product, brand, price, buy, purchase, model, specification, what is this, identify

## 🚀 How to Use

### In the Main Interface:
1. Upload an image
2. Select your desired analysis type from the dropdown
3. Click "Generate Analysis"
4. View detailed results
5. Optionally convert to audio narration

### In the Chatbot:
1. Upload an image in the chat interface
2. Ask specific questions about location or products
3. The system automatically uses specialized analysis
4. Get detailed, contextual responses

### Example Workflows:

**For Location Identification**:
1. Upload a travel photo
2. Select "Location Analysis"
3. Get detailed geographic and contextual information
4. Ask follow-up questions in the chatbot

**For Product Research**:
1. Upload a product photo
2. Select "Product Analysis"
3. Get brand, model, and market information
4. Ask specific questions about features or pricing

**For Complete Analysis**:
1. Upload any complex image
2. Select "Comprehensive Analysis"
3. Get detailed analysis of all elements
4. Use results for research or documentation

## 🎯 Best Practices

### For Better Location Analysis:
- Include landmarks or distinctive architecture
- Capture readable street signs or building names
- Show environmental context (surroundings, weather)
- Include multiple angles if possible

### For Better Product Analysis:
- Ensure good lighting and clear product visibility
- Include labels, tags, or packaging when possible
- Show brand logos or identifying marks clearly
- Capture any text or specifications visible

### For Better Text Extraction:
- Ensure text is clearly readable and well-lit
- Avoid blurry or distorted text
- Include context around the text
- Use high-resolution images when possible

## 🔧 Technical Details

### API Integration:
- Uses Google Gemini 1.5 Flash model
- Optimized prompts for each analysis type
- Lower temperature (0.3) for factual analysis
- Higher token limits for detailed responses

### Performance:
- Analysis typically takes 3-10 seconds
- Results are cached for the session
- Images are optimized before analysis
- Fallback handling for API errors

### Accuracy:
- Location analysis works best with distinctive features
- Product analysis is most accurate with clear branding
- Text extraction requires readable, well-lit text
- Comprehensive analysis provides balanced coverage

## 🛠️ Troubleshooting

### If Analysis Seems Inaccurate:
- Try a different analysis type
- Ensure image quality is good
- Check if the image contains the expected content
- Use the chatbot for follow-up questions

### If No Results:
- Verify your API key is set correctly
- Check internet connection
- Try with a different image
- Look for error messages in the interface

### For Better Results:
- Use high-quality, well-lit images
- Include context and identifying features
- Ask specific, detailed questions
- Try multiple analysis types for complex images