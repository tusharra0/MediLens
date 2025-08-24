import chromadb
import chromadb
client = chromadb.HttpClient(
  ssl=True,
  host='api.trychroma.com',
  tenant='c62ca6f6-ebde-4f3e-a727-885904e35df1',
  database='MediLens',
  headers={
    'x-chroma-token': 'ck-DhNfVgeXRLgL42wfYfSzqBbBs89Mbzp3gE4SCKrwX3as'
  }
)

