# MenuMind

MenuMind is a Streamlit front-end for an automated dietary and allergen review pipeline. A kitchen or restaurant owner submits a raw, unformatted menu and ingredient list; the submission is routed through an n8n workflow that audits every item for allergens and dietary classifications (vegan, vegetarian, gluten-free, hidden allergens like dairy/soy/shellfish/nuts), generates a structured PDF report, and emails it directly to the chef.

This repo contains only the front-end app. The review workflow itself runs in n8n and is not included here.

## How it works

1. The chef fills in the kitchen name, email, and menu/ingredient text in the Streamlit form.
2. On submit, the app POSTs the data as JSON to an n8n production webhook.
3. n8n runs the submission through an LLM-based allergen audit (Groq), builds a structured payload, and generates a PDF via APITemplate.io.
4. The finished PDF is emailed to the chef, and (if returned) a link to the PDF is shown back in the app.

```
[ Streamlit Form ] → [ n8n Webhook ] → [ Allergen Audit (Groq) ] → [ PDF Generation ] → [ Email to Chef ]
```

## Setup

### Requirements

- Python 3.9+
- An active n8n workflow with a webhook trigger (see workflow pipeline below)

### Install

```bash
pip install streamlit requests
```

### Configure the webhook URL

The app reads the n8n production webhook URL from an environment variable.

**Environment Variable**

```bash
export MENUMIND_WEBHOOK_URL="https://your-instance.app.n8n.cloud/webhook/...."
```

### Run locally

```bash
streamlit run app.py
```

## Payload format

The app sends the following JSON body to the n8n webhook:

```json
{
  "restaurant_name": "The Green Kitchen",
  "chef_email": "chef@example.com",
  "menu_text": "Garlic bread: wheat flour, butter, garlic, parsley\nTomato soup: tomatoes, vegetable stock, cream"
}
```

It expects an optional JSON response from n8n containing a `pdf_url` or `download_url` key to display a direct link to the generated PDF; otherwise the raw response is shown.

## Disclaimer

AI-generated allergen and dietary labels are a review aid, not a food-safety guarantee. Always verify ingredients, supplier labels, and cross-contact risks before serving or printing a final menu.

## License

Add a license of your choice (MIT, Apache-2.0, etc.) before making this repo public.
