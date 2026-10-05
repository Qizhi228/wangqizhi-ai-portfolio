# 腾讯云轻量服务器部署说明

当前目标主机是已通过 SSH 连接的 `tencent-lighthouse`。你还没有购买域名，因此先使用腾讯云轻量服务器公网 IP 访问；购买域名后再绑定域名和 HTTPS。

## 一、构建网站

在本地执行：

```bash
cd portfolio-site
npm install
npm run build
```

构建结果位于 `portfolio-site/dist/`。

## 二、服务器准备

在腾讯云服务器执行：

```bash
sudo apt update
sudo apt install -y nginx
sudo mkdir -p /var/www/wangqizhi-ai-portfolio
sudo chown -R "$USER":"$USER" /var/www/wangqizhi-ai-portfolio
```

## 三、上传网站

将本地 `dist/` 内容上传到服务器：

```bash
scp -r portfolio-site/dist/* USER@SERVER_IP:/var/www/wangqizhi-ai-portfolio/
```

把 `USER` 和 `SERVER_IP` 换成真实信息。不要把 SSH 私钥、模型 API Key 或 `.env` 上传到网站目录。

## 四、配置 Nginx

创建站点配置：

```nginx
server {
    listen 80;
    server_name _;

    root /var/www/wangqizhi-ai-portfolio;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

启用配置并检查：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

然后在腾讯云控制台放行安全组 TCP 80 端口，用浏览器访问服务器公网 IP。

## 五、购买域名后的操作

1. 在腾讯云 DNSPod 添加 A 记录，指向服务器公网 IP。
2. 将 Nginx 中的 `server_name _;` 改成你的域名。
3. 使用腾讯云证书或 Certbot 配置 HTTPS。
4. 将作品集网站中的 GitHub 链接、邮箱和到岗状态更新为真实信息。

## 安全检查

- 不要把 `.env` 上传到 GitHub 或服务器网站目录。
- 不要把模型 API Key 写入 Vue 前端。
- 公开仓库只使用自造数据。
- 上传前确认没有实习公司的文档、截图和源代码。
