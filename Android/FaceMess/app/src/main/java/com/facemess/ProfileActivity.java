package com.facemess;

import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

import java.util.ArrayList;

/**
 * Created by Danish Shah on 13-08-2017.
 */

public class ProfileActivity extends AppCompatActivity {

    RecyclerView collection_rv;

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        ArrayList<String> arr_list = new ArrayList<>();

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        toolbar.setElevation(0);

        toolbar.setTitle("@da9ish");

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        for (int i=0;i<10;i++)
            arr_list.add(i+"");

        collection_rv = (RecyclerView) findViewById(R.id.collection_rv);

        collection_rv.setAdapter(new CollectionAdapter(arr_list, this));
        collection_rv.setLayoutManager(new GridLayoutManager(this, 2));


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_profile, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            startActivity(new Intent(ProfileActivity.this, SettingsAcitvity.class));
        }

        return super.onOptionsItemSelected(item);
    }

    class CollectionAdapter extends RecyclerView.Adapter<CollectionViewHolder>{

        ArrayList<String> list;
        Context cxt;

        public CollectionAdapter(ArrayList<String> list, Context cxt) {
            this.list = list;
            this.cxt = cxt;
        }

        @Override
        public CollectionViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {

            View v = LayoutInflater.from(cxt).inflate(R.layout.item_collection, parent, false);

            return new CollectionViewHolder(v);
        }

        @Override
        public void onBindViewHolder(CollectionViewHolder holder, int position) {

            holder.collection.setBackgroundColor(getResources().getColor(R.color.colorAccent));
        }

        @Override
        public int getItemCount() {
            return list.size();
        }
    }

    class CollectionViewHolder extends RecyclerView.ViewHolder{

        LinearLayout collection;

        public CollectionViewHolder(View itemView) {
            super(itemView);

            collection = (LinearLayout) itemView.findViewById(R.id.collection_item);
        }
    }
}
