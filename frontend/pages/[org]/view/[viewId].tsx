import Link from 'next/link';
import Head from 'next/head';
import Layout from '../../../components/layout';

import { useRouter } from 'next/router'
import useSWR from 'swr'

import dynamic from 'next/dynamic'
import React from 'react';
import BaseEntityView from './baseEntityView';

function DynamicHeader(path) {
    return dynamic(() => import(path), {
        loading: () => 'Loading...',
    })
}

const fetcher = (param) => fetch(param.url, param.args).then(res => res.json())

const viewComponents = {
    'com.freelearning.base.entity': './baseEntityView',
}

export default function View() {
    const router = useRouter()
    const { org, viewId } = router.query
    const entityId = viewId ? viewId : '0' // 844424930135849

    const sendData = {
        start_properties: {'route': 'web/test'},
        link_label: 'com.freelearning.base.NEXT_OF',
        end_entity_id: entityId,
    }
    const { data, error, isLoading } = useSWR(
        router.isReady? {
            url: 'http://localhost:8000/api/com.freelearning.base/v1/query-linked/',
            args: {
                method: 'POST',
                body: JSON.stringify(sendData),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        } : null, fetcher);

    const sendData2 = {
        link_label: 'com.freelearning.base.CHILD_OF',
        end_entity_id: entityId,
    }
    const { data: xdata, error: xerror, isLoading: isLoading2 } = useSWR(
        router.isReady? {
            url: 'http://localhost:8000/api/com.freelearning.base/v1/query-linked/',
            args: {
                method: 'POST',
                body: JSON.stringify(sendData2),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        } : null, fetcher);

    console.log('PID', org, viewId, entityId, isLoading, data, xdata)

    if (isLoading || isLoading2) return <p>Loading</p>

    // const name = 'first-post';
    // const props = { count: 'value1', prop2: 'value2' };
    // return initComponent(name, props);
    const items = data?.query_result?.[0]?.map((entry) => {
        const entity = entry
        if (entity.label == "com.freelearning.base.entity") {
            return <BaseEntityView {...entity} />
        } else {

        }
    });
    // const items2 = xdata?.query_result?.map((entry) =>
    //     console.log(entry[0], 'x'))
    // const items2 = xdata?.query_result?.map((entry) =>
    //     initComponent(viewComponents[entry[0].label], entry[0]))
    const items2 = xdata?.query_result?.map((entry) => {
        const entity = entry[0]
        if (entity.label == "com.freelearning.base.entity") {
            return <BaseEntityView {...entity} />
        } else {

        }
    })
    return (
        <Layout>

        <Head>
            <title>First Post</title>
            </Head>

            <div>{items}</div>
            <div>{items2}</div>

        </Layout>
    );
}
