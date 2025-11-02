from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('PINECONE_INDEX_NAME', 'babybot-medical-index')

if not api_key:
    print('PINECONE_API_KEY not set. Aborting.')
    exit(1)

pc = Pinecone(api_key=api_key)
if index_name not in [idx['name'] for idx in pc.list_indexes()]:
    print(f'Index {index_name} does not exist. Nothing to delete.')
    exit(0)

idx = pc.Index(index_name)
print(f'Deleting ALL vectors from index: {index_name} (this is irreversible)')
idx.delete(delete_all=True)
print('Delete command issued.')

# Try to fetch stats
try:
    stats = idx.describe_index_stats()
    print('Index stats after deletion:', stats)
except Exception as e:
    print('Could not fetch stats:', e)
