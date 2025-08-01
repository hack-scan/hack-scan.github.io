# 安卓某APP登陆逆向

<!--more-->

# APP抓包捕获登陆参数

因为没有网页端，只能在手机抓包或流量转发到电脑，手机Root过所以直接用手机。

![image-20250505235820030](https://fastly.jsdelivr.net/gh/hack-scan/Blog-pic/posts/202505271935183.png)

```txt
loginType=RPQQrpdg4Fes4KNvy3Y%2B%2BpOI0A%2FylWUapwSE2BvKtkzcEM8bR%2BGtScJG4ddJ8MKV%2BRHL%2BhpQG4yt%0ADq%2Ff%2FzY7P9eP%2B94EBELbYL89R7UXjw%2BRD5BPJxeoduW37iJKLV25CuDMcmHlu3Y6hYsT1NSEqXdV%0APjGDPz8mYx7e8fxB6yc%3D%0A
username=aNIrmXtw8nx6tVE******
password=X3WBkR13dBwKYc9KTYS0qgxts9O6jxhzBB%2FEB2kbKQY8VyN5g8exakcZZ64k1wKBlMit3XORAAFB%0AqHIzRb9YJoR6gsX9C2hXPmKjJcIEYHZLQE%2BjO5wT9zHF%2FZ0oUqVbREA3PiT97JwXIsd3Y8wYCTk6%0Aeq2fE6vrMr4oB2uabcY%3D%0A
deviceModel=bGUK%2F8im%2FzPxcVzR1lO7HxvVzxzNAnIrhwv87GqQwigL1fPVfaOBdnkYxRVkSce7UdcKFh7YLtis%0AnGzt98FD2aOxsQ3J%2FYifNAgMmaIIhA6I3vr4%2Fs2FU83NRqCghW0QRUNp28oJMvBgnUTexv4bYPmq%0AdLf7RZDF1mh0nncYVSY%3D%0A
devType=YcDlQYgnt0f%2FNAlEbYOKQUl9TZJD0SeR15iMoKahSu7E3Oj2549jSPwRxR3l2f11DGM2lkVLTs%2Bn%0A43WTazF3WM5pJ9n3W65TW3mc1COHzvI92WkcOAhEgol3mMi6uhdaHmQahKAd708ETv5VZvIN63Fm%0AYjMoq07ABgXG7714gIw%3D%0A
opertionSystem=JrVdi%2BqF1C4SsRKTDUGhhTq0ScdbynezoR2JDVXLTbaQ6cVNPl4o2z6hkhwuRjN270yM7FKucQWI%0AE2gbnvMOpqn42FIn2FIxnhW0vgUxYxRCli186XVNZ72h8eT6AlEH0KDF6dMcJ76L8VAdR5UmZMyV%0ArsVAA77uOefjy6rzKVM%3D%0A
ipAddress=l6zP%2FQp5sam3BIemhFGSkS7tMDzoW4OcAM6Ws%2FKdYW9yTVWzYc%2BU%2BKwdhowy1tUOXnRceLMg3D6c%0AUYo4F%2BVdqxse7i7XYoUFn%2B10qFo%2BwgaQtFnjSgqOEu4B3VYALsapRyUioarab8ZiYnotaDvxW1%2FL%0A6wGwa%2BvaeJIqH0oiXDA%3D%0A
devId=VdBEdtsRKLx70vdYe%2F1g******
```

### Url解码获取原始结果

复制下来有`%`，一眼就是URL，先URL解码

```python
import urllib.parse
data = {
    "ipAddress": "l6zP/Qp5sam3BIemhFGSkS7tMDzoW4OcAM6Ws/KdYW9yTVWzYc%2BU%2BKwdhowy1tUOXnRceLMg3D6cUYo4F%2BVdqxse7i7XYoUFn%2B10qFo%2BwgaQtFnjSgqOEu4B3VYALsapRyUioarab8ZiYnotaDvxW1/L6wGwa%2BvaeJIqH0oiXDA%3D",
}
#解码打印

for key, value in data.items():
    decoded = urllib.parse.unquote(value.replace("\n", ""))
    print(f"{key} = {decoded}\n")
```

## 还原加解密

### 算法助手抓包获取加密参数

![](https://fastly.jsdelivr.net/gh/hack-scan/Blog-pic/posts/202505271959519.png)

拿到密钥开始还原加解密，但是每次加密结果是不一样的，加密算法是RSA随机填充序列，我们只有解密可以验证密钥是否可用

### 解密代码

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode

# 你的私钥和公钥（Base64 格式）
private_key_b64 = """
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALdWyfoa5KK9tzSaHVAUOMVUx2RvuVwB+wZ3Dpa5HTIzgYE/kwImvfTVVflpC5w4qamelHiaExJoIbQBVsr1UE2WCEVyKF+fe7i4w8a2q1fMpIk1mYuvOtLtd3R5xRwAYcCekSddeChShisCS2HApMENrIQjKBAGur6cxfneBJP1AgMBAAECgYAqmaP81Vri5ao4Msc04D4AvB5InB0538vwSKG/K+w4yfcBjUAfc9kXlqqPdXUZK6FgpFRjYYmk8UVDijwclLu/pmRWXqMozlgE2Xbx+r5psxcbzXBIzeNx46eLHB6huOkttBZgknB2iKjJT/lJZ+1bPlaTxYdpmYCM20tHZKMjgQJBAOsn0l0ckRcFt+NICDdNfj+Pd14L/9Enu9aeQ81KI7L6Qygv+I1EduwY4jtub0TZy3fiyeVDwRq5Hby08hLqInkCQQDHlyPip3y9CEYSJDN5gn2aP6dzsXwHSpIYPIf2fMErZaFqvrV9in1ERzDTMT+o70kKbTsUng1pC4p8RflWUv5dAkEAs9DVmYG4qMQko1V3guJtAalw+6dtTMB3cFvBOP/SYI/iPp7ADzYlQdCdXhjKWPm6DsiK3hd7WDXpuV0cJr6G8QJAU1FWm6FLQyYXCi+uhUTh5eg4oOUwX2LTxeZO46iEgvc0APmHjdaoID6PtTnT11O8a+vZQ+wOsREuSF51jYGryQJAdglyLFsbUSMN8jdh6E0HYgYbKU5n6wnSBmLK5F81brytIbJID7bA0K5hj4TOCzjcE7VDzTCHd20sofPnU4zhFA==
""".replace("\n", "")

public_key_b64 = """
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3Vsn6GuSivbc0mh1QFDjFVMdkb7lcAfsGdw6WuR0yM4GBP5MCJr301VX5aQucOKmpnpR4mhMSaCG0AVbK9VBNlghFcihfn3u4uMPGtqtXzKSJNZmLrzrS7Xd0ecUcAGHAnpEnXXgoUoYrAkthwKTBDayEIygQBrq+nMX53gST9QIDAQAB
""".replace("\n", "")

# 生成私钥和公钥对象
private_key = RSA.importKey(b64decode(private_key_b64))
public_key = RSA.importKey(b64decode(public_key_b64))

def encrypt_with_public_key(plain_text: str) -> str:
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(plain_text.encode('utf-8'))
    return b64encode(encrypted).decode()

def decrypt_with_private_key(cipher_text_b64: str) -> str:
    cipher = PKCS1_v1_5.new(private_key)
    encrypted_bytes = b64decode(cipher_text_b64)
    sentinel = b"error"
    decrypted = cipher.decrypt(encrypted_bytes, sentinel)
    return decrypted.decode()

plain = "scan.work"
enc = encrypt_with_public_key(plain)
dec = decrypt_with_private_key(enc)

print("原文:", plain)
print("加密后:", enc)
print("解密后:", dec)
```

之前这个站有任意文件下载漏洞，所以把打包的源码下载到本地过，我们查看一下反编译的Class

![image-20250505114930388](https://fastly.jsdelivr.net/gh/hack-scan/Blog-pic/posts/202505271943901.png)

有私钥公钥且私钥与算法助手获取的一致，审计源码可知，都是公钥加密，私钥解密的。

### 加密代码

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode

# 你的私钥和公钥（Base64 格式）
private_key_b64 = """
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALdWyfoa5KK9tzSaHVAUOMVUx2RvuVwB+wZ3Dpa5HTIzgYE/kwImvfTVVflpC5w4qamelHiaExJoIbQBVsr1UE2WCEVyKF+fe7i4w8a2q1fMpIk1mYuvOtLtd3R5xRwAYcCekSddeChShisCS2HApMENrIQjKBAGur6cxfneBJP1AgMBAAECgYAqmaP81Vri5ao4Msc04D4AvB5InB0538vwSKG/K+w4yfcBjUAfc9kXlqqPdXUZK6FgpFRjYYmk8UVDijwclLu/pmRWXqMozlgE2Xbx+r5psxcbzXBIzeNx46eLHB6huOkttBZgknB2iKjJT/lJZ+1bPlaTxYdpmYCM20tHZKMjgQJBAOsn0l0ckRcFt+NICDdNfj+Pd14L/9Enu9aeQ81KI7L6Qygv+I1EduwY4jtub0TZy3fiyeVDwRq5Hby08hLqInkCQQDHlyPip3y9CEYSJDN5gn2aP6dzsXwHSpIYPIf2fMErZaFqvrV9in1ERzDTMT+o70kKbTsUng1pC4p8RflWUv5dAkEAs9DVmYG4qMQko1V3guJtAalw+6dtTMB3cFvBOP/SYI/iPp7ADzYlQdCdXhjKWPm6DsiK3hd7WDXpuV0cJr6G8QJAU1FWm6FLQyYXCi+uhUTh5eg4oOUwX2LTxeZO46iEgvc0APmHjdaoID6PtTnT11O8a+vZQ+wOsREuSF51jYGryQJAdglyLFsbUSMN8jdh6E0HYgYbKU5n6wnSBmLK5F81brytIbJID7bA0K5hj4TOCzjcE7VDzTCHd20sofPnU4zhFA==
""".replace('\n', '')

public_key_b64 = """
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3Vsn6GuSivbc0mh1QFDjFVMdkb7lcAfsGdw6WuR0yM4GBP5MCJr301VX5aQucOKmpnpR4mhMSaCG0AVbK9VBNlghFcihfn3u4uMPGtqtXzKSJNZmLrzrS7Xd0ecUcAGHAnpEnXXgoUoYrAkthwKTBDayEIygQBrq+nMX53gST9QIDAQAB
""".replace('\n', '')

# 生成私钥和公钥对象
private_key = RSA.importKey(b64decode(private_key_b64))
public_key = RSA.importKey(b64decode(public_key_b64))

def encrypt_with_public_key(plain_text: str) -> str:
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(plain_text.encode('utf-8'))
    return b64encode(encrypted).decode()

def decrypt_with_private_key(cipher_text_b64: str) -> str:
    cipher = PKCS1_v1_5.new(private_key)
    encrypted_bytes = b64decode(cipher_text_b64)
    sentinel = b'error'
    decrypted = cipher.decrypt(encrypted_bytes, sentinel)
    return decrypted.decode()

plain = "scan.work"
enc = encrypt_with_public_key(plain)
dec = decrypt_with_private_key(enc)

print("原文:", plain)
print("加密后:", enc)
print("解密后:", dec)
```

## 尝试还原登陆结果

![image-20250505120546842](https://fastly.jsdelivr.net/gh/hack-scan/Blog-pic/posts/202505271942275.png)

成功获取Token


---

> 作者: [Scan](https://www.scan.work/)  
> URL: https://5canx.github.io/posts/%E5%AE%89%E5%8D%93%E6%9F%90app%E7%99%BB%E9%99%86%E9%80%86%E5%90%91/  

