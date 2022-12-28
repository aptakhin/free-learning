import Link from 'next/link';
import Head from 'next/head';
import Script from 'next/script';
import Layout from '../components/layout';
import initComponent from './[org]/view/init-component';

export default function SecondPost() {
    const name = 'first-post';
    const props = { count: 'value1', prop2: 'value2' };
    return initComponent(name, props);
}
