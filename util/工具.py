import hashlib

def sha256_hash(text: str) -> str:
    """计算字符串的 SHA-256 哈希值"""
    return hashlib.sha256(text.encode()).hexdigest()
