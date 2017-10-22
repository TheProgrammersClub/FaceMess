package com.facemess;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.Camera;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

import de.hdodenhof.circleimageview.CircleImageView;

import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    Camera camera, fcamera;
    CameraPreview preview, fpreview;
    List<Camera.Size> supportedPreviewSizes;
    Camera.Size previewSize;
    Button capture;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        CircleImageView prof_iamge = (CircleImageView) findViewById(R.id.profile_image);
        prof_iamge.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, ProfileActivity.class));
            }
        });


        if (Build.VERSION.SDK_INT >= 23)
            getCameraPermission();
        else {
            if (checkCamera(this)) {

                supportedPreviewSizes = camera.getParameters().getSupportedPreviewSizes();


                camera = getCameraInstance(0);

                preview = new CameraPreview(this, camera);

                FrameLayout container = (FrameLayout) findViewById(R.id.preview_container);
                container.addView(preview);



//                fcamera = getCameraInstance(findFrontCamera());
//
//                fpreview = new CameraPreview(this, fcamera);
//
//                FrameLayout fcontainer = (FrameLayout) findViewById(R.id.f_preview_container);
//                fcontainer.addView(fpreview);


            }
        }

        capture = (Button) findViewById(R.id.capture_btn);
        capture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                camera.takePicture(shutterCallback, null, pictureCallback);
            }
        });


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_profile) {
            startActivity(new Intent(MainActivity.this, ProfileActivity.class));
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    Camera.ShutterCallback shutterCallback = new Camera.ShutterCallback() {
        @Override
        public void onShutter() {

        }
    };

    Camera.PictureCallback pictureCallback = new Camera.PictureCallback() {
        @Override
        public void onPictureTaken(byte[] data, Camera camera) {

            File pictureFile = new File(String.valueOf(MEDIA_TYPE_IMAGE));
            if (pictureFile == null){
                Log.d(TAG, "Error creating media file, check storage permissions: ");
                return;
            }

            try {
                FileOutputStream fos = new FileOutputStream(pictureFile);
                fos.write(data);
                fos.close();
            } catch (FileNotFoundException e) {
                Log.d(TAG, "File not found: " + e.getMessage());
            } catch (IOException e) {
                Log.d(TAG, "Error accessing file: " + e.getMessage());
            }
        }
    };



    public void getCameraPermission(){

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED){
            if (checkCamera(this)) {
                camera = getCameraInstance(0);

                preview = new CameraPreview(this, camera);

                FrameLayout container = (FrameLayout) findViewById(R.id.preview_container);
                container.addView(preview);

//                fcamera = getCameraInstance(findFrontCamera());
//
//                fpreview = new CameraPreview(this, fcamera);
//
//                FrameLayout fcontainer = (FrameLayout) findViewById(R.id.f_preview_container);
//                fcontainer.addView(fpreview);
            }
        }else {
            ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1010);

        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode){
            case 1010:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    if (checkCamera(this)) {
                        camera = getCameraInstance(0);

                        preview = new CameraPreview(this, camera);

                        FrameLayout container = (FrameLayout) findViewById(R.id.preview_container);
                        container.addView(preview);

//                        fcamera = getCameraInstance(findFrontCamera());
//
//                        fpreview = new CameraPreview(this, fcamera);
//
//                        FrameLayout fcontainer = (FrameLayout) findViewById(R.id.f_preview_container);
//                        fcontainer.addView(fpreview);
                    }
                }
        }
    }

    public boolean checkCamera(Context cxt) {
        if (cxt.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            Log.d(TAG, "Camera Available");
            return true;
        } else {
            Log.d(TAG, "Camera Unavailable");
            return false;
        }
    }

    public static Camera getCameraInstance(int id) {
        Camera c = null;

        try {
            c = Camera.open(id);
            Log.d(TAG, c.getParameters().toString());
        } catch (Exception e) {
            // Camera is not available (in use or does not exist)
        }

        return c;
    }

    public int findFrontCamera() {
        int cameraId = -1;
        // Search for the front facing camera
        int numberOfCameras = Camera.getNumberOfCameras();
        for (int i = 0; i < numberOfCameras; i++) {
            Camera.CameraInfo info = new Camera.CameraInfo();
            Camera.getCameraInfo(i, info);
            if (info.facing == Camera.CameraInfo.CAMERA_FACING_FRONT) {
                Log.d(TAG, "Camera found");
                cameraId = i;
                break;
            }
        }
        return cameraId;
    }

    public Camera.Size getOptimalPreviewSize(List<Camera.Size> sizes, int w, int h) {
        final double ASPECT_TOLERANCE = 0.1;
        double targetRatio=(double)h / w;

        if (sizes == null) return null;

        Camera.Size optimalSize = null;
        double minDiff = Double.MAX_VALUE;

        int targetHeight = h;

        for (Camera.Size size : sizes) {
            double ratio = (double) size.width / size.height;
            if (Math.abs(ratio - targetRatio) > ASPECT_TOLERANCE) continue;
            if (Math.abs(size.height - targetHeight) < minDiff) {
                optimalSize = size;
                minDiff = Math.abs(size.height - targetHeight);
            }
        }

        if (optimalSize == null) {
            minDiff = Double.MAX_VALUE;
            for (Camera.Size size : sizes) {
                if (Math.abs(size.height - targetHeight) < minDiff) {
                    optimalSize = size;
                    minDiff = Math.abs(size.height - targetHeight);
                }
            }
        }
        return optimalSize;
    }

    public class CameraPreview extends SurfaceView implements SurfaceHolder.Callback{

        SurfaceHolder holder;
        Camera camera;

        public CameraPreview(Context context, Camera camera) {
            super(context);

            this.camera = camera;

            holder = getHolder();
            holder.addCallback(this);

            holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
        }

        @Override
        public void surfaceCreated(SurfaceHolder holder) {

            try {
                camera.setDisplayOrientation(90);
                camera.setPreviewDisplay(holder);
                camera.startPreview();
//                camera.startFaceDetection();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
            if (holder.getSurface() == null){
                // preview surface does not exist
                return;
            }

            // stop preview before making changes
            try {
                camera.stopPreview();
            } catch (Exception e){
                // ignore: tried to stop a non-existent preview
            }

            // set preview size and make any resize, rotate or
            // reformatting changes here

            // start preview with new settings
            try {
                camera.setPreviewDisplay(holder);
                Camera.Parameters parameters = camera.getParameters();
//                parameters.setPreviewSize(previewSize.width, previewSize.height);
//                camera.setParameters(parameters);
                camera.startPreview();

            } catch (Exception e){
                Log.d(TAG, "Error starting camera preview: " + e.getMessage());
            }
        }

        @Override
        public void surfaceDestroyed(SurfaceHolder holder) {
            camera.release();
        }

        @Override
        protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
            final int width = resolveSize(getSuggestedMinimumWidth(), widthMeasureSpec);
            final int height = resolveSize(getSuggestedMinimumHeight(), heightMeasureSpec);
            setMeasuredDimension(width, height);

            if (supportedPreviewSizes != null) {
                previewSize = getOptimalPreviewSize(supportedPreviewSizes, width, height);
            }
        }
    }
}
