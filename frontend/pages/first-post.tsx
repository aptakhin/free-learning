import Link from 'next/link';
import Head from 'next/head';
import Script from 'next/script';
import Layout from '../components/layout';

export default function FirstPost({ count }) {
    return (
        <Layout>
            <style jsx>{`
        h1 {
          color: blue;
        }
        div {
          background: red;
        }
        @media (max-width: 600px) {
          div {
            background: blue;
          }
        }
      `}</style>
        <Head>
                <title>First Post {count}</title>

            </Head>
            <Script
        src="https://connect.facebook.net/en_US/sdk.js"
        strategy="lazyOnload"
        onLoad={() =>
          console.log(`script loaded correctly, window.FB has been populated`)
        }
      />
        <h1>First Post</h1>
        <h2>
          <Link href="/">← Back to home</Link>
        </h2>
        </Layout>

    );
  }
